from flask import Flask, render_template, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
from youtube_transcript_api.formatters import TextFormatter
import google.generativeai as genai
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from textblob import TextBlob
from dotenv import load_dotenv
import os
import re
import time
import yt_dlp
import json
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from rouge_score import rouge_scorer
import pandas as pd
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please create a .env file with your API key.")

genai.configure(api_key=GEMINI_API_KEY)


def preprocess_text(text, apply_preprocessing=True):
    """
    Preprocess text with tokenization, stop-word removal, and normalization.
    Phase 1: NLP Preprocessing Pipeline for Academic Requirements
    
    Args:
        text (str): Raw text to preprocess
        apply_preprocessing (bool): Whether to apply preprocessing steps
    
    Returns:
        str: Preprocessed text (or original if apply_preprocessing=False)
    """
    if not apply_preprocessing:
        return text
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Tokenization
    tokens = word_tokenize(text)
    
    # Remove stop words
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in tokens if token not in stop_words and token.strip()]
    
    # Rejoin tokens
    preprocessed_text = ' '.join(filtered_tokens)
    
    return preprocessed_text


def get_youtube_comments(video_id, max_comments=100):
    """Fetch comments from a YouTube video"""
    if not YOUTUBE_API_KEY:
        return None, "YOUTUBE_API_KEY not configured. Add it to .env file to enable comment analysis."
    
    try:
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        comments = []
        
        request = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=min(max_comments, 100),
            order='relevance',
            textFormat='plainText'
        )
        
        response = request.execute()
        
        for item in response.get('items', []):
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append({
                'text': comment['textDisplay'],
                'author': comment['authorDisplayName'],
                'likes': comment['likeCount'],
                'published': comment['publishedAt']
            })
        
        return comments, None
        
    except HttpError as e:
        if e.resp.status == 403:
            return None, "YouTube API quota exceeded or comments are disabled for this video."
        return None, f"Error fetching comments: {str(e)}"
    except Exception as e:
        return None, f"Error fetching comments: {str(e)}"


def analyze_sentiment(comments):
    """Perform sentiment analysis on comments using TextBlob"""
    if not comments:
        return None
    
    sentiments = []
    for comment in comments:
        blob = TextBlob(comment['text'])
        polarity = blob.sentiment.polarity  # -1 (negative) to 1 (positive)
        
        # Classify sentiment
        if polarity > 0.1:
            sentiment = 'positive'
        elif polarity < -0.1:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        sentiments.append({
            'text': comment['text'][:100] + '...' if len(comment['text']) > 100 else comment['text'],
            'author': comment['author'],
            'sentiment': sentiment,
            'polarity': round(polarity, 3),
            'likes': comment['likes']
        })
    
    # Calculate overall statistics
    total = len(sentiments)
    positive = sum(1 for s in sentiments if s['sentiment'] == 'positive')
    negative = sum(1 for s in sentiments if s['sentiment'] == 'negative')
    neutral = sum(1 for s in sentiments if s['sentiment'] == 'neutral')
    avg_polarity = sum(s['polarity'] for s in sentiments) / total if total > 0 else 0
    
    return {
        'comments': sentiments,
        'statistics': {
            'total': total,
            'positive': positive,
            'negative': negative,
            'neutral': neutral,
            'positive_percent': round((positive / total) * 100, 1) if total > 0 else 0,
            'negative_percent': round((negative / total) * 100, 1) if total > 0 else 0,
            'neutral_percent': round((neutral / total) * 100, 1) if total > 0 else 0,
            'average_polarity': round(avg_polarity, 3)
        }
    }


def extract_video_id(url):
    """Extract YouTube video ID from various URL formats"""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)',
        r'youtube\.com\/embed\/([^&\n?#]+)',
        r'youtube\.com\/v\/([^&\n?#]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def get_transcript_ytdlp(video_id):
    """Fallback method to get transcript using yt-dlp"""
    try:
        ydl_opts = {
            'skip_download': True,
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': ['en'],
            'subtitlesformat': 'json3',
            'quiet': True,
            'no_warnings': True,
        }
        
        url = f'https://www.youtube.com/watch?v={video_id}'
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Try to get subtitles
            if 'subtitles' in info and 'en' in info['subtitles']:
                # Get the subtitle URL
                sub_url = info['subtitles']['en'][0]['url']
                import urllib.request
                with urllib.request.urlopen(sub_url) as response:
                    sub_data = json.loads(response.read().decode())
                    # Extract text from JSON3 format
                    text_parts = []
                    for event in sub_data.get('events', []):
                        if 'segs' in event:
                            for seg in event['segs']:
                                if 'utf8' in seg:
                                    text_parts.append(seg['utf8'])
                    return ' '.join(text_parts), None
            
            # Try automatic captions
            if 'automatic_captions' in info and 'en' in info['automatic_captions']:
                sub_url = info['automatic_captions']['en'][0]['url']
                import urllib.request
                with urllib.request.urlopen(sub_url) as response:
                    sub_data = json.loads(response.read().decode())
                    text_parts = []
                    for event in sub_data.get('events', []):
                        if 'segs' in event:
                            for seg in event['segs']:
                                if 'utf8' in seg:
                                    text_parts.append(seg['utf8'])
                    return ' '.join(text_parts), None
            
            return None, "No subtitles found for this video."
            
    except Exception as e:
        return None, f"yt-dlp error: {str(e)}"


def get_transcript(video_id):
    """Fetch transcript for a YouTube video"""
    
    # Try youtube-transcript-api first (faster)
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        transcript_text = ' '.join([entry['text'] for entry in transcript_list])
        return transcript_text, None
    except:
        try:
            # Try any language
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            transcript_text = ' '.join([entry['text'] for entry in transcript_list])
            return transcript_text, None
        except:
            pass
    
    # If youtube-transcript-api fails, try yt-dlp as fallback
    print(f"youtube-transcript-api failed, trying yt-dlp for video {video_id}")
    return get_transcript_ytdlp(video_id)


def summarize_with_gemini(transcript, temperature=0.7, length="medium", apply_preprocessing=False, model_name='models/gemini-2.0-flash'):
    """Summarize the transcript using Gemini API"""
    try:
        # Apply preprocessing if requested
        processed_transcript = preprocess_text(transcript, apply_preprocessing)
        
        # Configure safety settings to be more permissive for educational content
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE"
            }
        ]
        
        model = genai.GenerativeModel(
            model_name=model_name,
            safety_settings=safety_settings
        )
        
        # Define length-specific prompts
        length_prompts = {
            "concise": "Provide a brief, concise summary in 2-3 sentences covering only the most important points",
            "medium": "Provide a balanced summary covering the main points, key takeaways, and important details",
            "detailed": "Provide a comprehensive, detailed summary with all main points, supporting details, key examples, and important takeaways organized in clear sections"
        }
        
        prompt_instruction = length_prompts.get(length, length_prompts["medium"])
        
        prompt = f"""{prompt_instruction} of the following video transcript:

        {processed_transcript}
        
        Summary:"""
        
        generation_config = genai.types.GenerationConfig(
            temperature=temperature,
            max_output_tokens=2048,
        )
        
        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )
        
        # Check if response was blocked or has no text
        if not response.text or response.text.strip() == "":
            # Check finish reason
            if hasattr(response, 'candidates') and response.candidates:
                finish_reason = response.candidates[0].finish_reason
                safety_ratings = response.candidates[0].safety_ratings if hasattr(response.candidates[0], 'safety_ratings') else []
                
                error_msg = f"Content generation blocked (finish_reason: {finish_reason})"
                if safety_ratings:
                    error_msg += f". Safety ratings: {safety_ratings}"
                return None, error_msg
            return None, "No content generated (empty response)"
        
        return response.text, None
    except Exception as e:
        error_msg = str(e)
        # Extract more specific error information if available
        if "finish_reason" in error_msg.lower():
            return None, f"Invalid operation: {error_msg}"
        return None, f"Error generating summary: {error_msg}"


@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process_video():
    """Process the YouTube video URL"""
    data = request.json
    url = data.get('url', '').strip()
    temperature = float(data.get('temperature', 0.7))
    length = data.get('length', 'medium')
    analyze_comments = data.get('analyze_comments', False)
    apply_preprocessing = data.get('apply_preprocessing', False)
    
    if not url:
        return jsonify({'error': 'Please provide a YouTube URL'}), 400
    
    # Extract video ID
    video_id = extract_video_id(url)
    if not video_id:
        return jsonify({'error': 'Invalid YouTube URL'}), 400
    
    # Get transcript
    transcript, error = get_transcript(video_id)
    if error:
        return jsonify({'error': error}), 400
    
    # Generate summary
    summary, error = summarize_with_gemini(transcript, temperature, length, apply_preprocessing)
    if error:
        return jsonify({'error': error}), 500
    
    result = {
        'transcript': transcript,
        'summary': summary,
        'video_id': video_id,
        'preprocessing_applied': apply_preprocessing
    }
    
    # Get and analyze comments if requested
    if analyze_comments:
        comments, error = get_youtube_comments(video_id)
        if error:
            result['comment_analysis'] = {'error': error}
        elif comments:
            sentiment_analysis = analyze_sentiment(comments)
            result['comment_analysis'] = sentiment_analysis
        else:
            result['comment_analysis'] = {'error': 'No comments found'}
    
    return jsonify(result)


@app.route('/evaluate', methods=['POST'])
def evaluate_models():
    """Evaluate multiple Gemini models with ROUGE scores and performance metrics"""
    data = request.json
    url = data.get('url', '').strip()
    temperature = float(data.get('temperature', 0.7))
    length = data.get('length', 'medium')
    apply_preprocessing = data.get('apply_preprocessing', False)
    
    if not url:
        return jsonify({'error': 'Please provide a YouTube URL'}), 400
    
    # Extract video ID
    video_id = extract_video_id(url)
    if not video_id:
        return jsonify({'error': 'Invalid YouTube URL'}), 400
    
    # Get transcript
    transcript, error = get_transcript(video_id)
    if error:
        return jsonify({'error': error}), 400
    
    # Models to compare - using available models that support generateContent
    models_to_test = [
        'models/gemini-2.0-flash-exp',      # Latest experimental flash model
        'models/gemini-2.5-flash',          # Fast, efficient model
        'models/gemini-2.5-pro'             # High quality pro model
    ]
    
    results = []
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    
    # Reference: Use first 1000 words of transcript as reference for ROUGE
    reference_text = ' '.join(transcript.split()[:1000])
    
    for model_name in models_to_test:
        try:
            # Measure processing time
            start_time = time.time()
            summary, error = summarize_with_gemini(transcript, temperature, length, apply_preprocessing, model_name)
            processing_time = time.time() - start_time
            
            if error:
                results.append({
                    'model': model_name,
                    'error': error,
                    'processing_time': processing_time
                })
                continue
            
            # Calculate ROUGE scores
            rouge_scores = scorer.score(reference_text, summary)
            
            # Calculate compression ratio
            original_words = len(transcript.split())
            summary_words = len(summary.split())
            compression_ratio = round((summary_words / original_words) * 100, 2)
            
            results.append({
                'model': model_name,
                'summary': summary,
                'processing_time': round(processing_time, 3),
                'metrics': {
                    'rouge1': {
                        'precision': round(rouge_scores['rouge1'].precision, 4),
                        'recall': round(rouge_scores['rouge1'].recall, 4),
                        'fmeasure': round(rouge_scores['rouge1'].fmeasure, 4)
                    },
                    'rouge2': {
                        'precision': round(rouge_scores['rouge2'].precision, 4),
                        'recall': round(rouge_scores['rouge2'].recall, 4),
                        'fmeasure': round(rouge_scores['rouge2'].fmeasure, 4)
                    },
                    'rougeL': {
                        'precision': round(rouge_scores['rougeL'].precision, 4),
                        'recall': round(rouge_scores['rougeL'].recall, 4),
                        'fmeasure': round(rouge_scores['rougeL'].fmeasure, 4)
                    },
                    'compression_ratio': compression_ratio,
                    'original_words': original_words,
                    'summary_words': summary_words
                }
            })
            
        except Exception as e:
            results.append({
                'model': model_name,
                'error': str(e),
                'processing_time': 0
            })
    
    return jsonify({
        'video_id': video_id,
        'transcript_length': len(transcript.split()),
        'models_evaluated': len(results),
        'results': results
    })


@app.route('/sentiment-metrics', methods=['GET'])
def get_sentiment_metrics():
    """Get sentiment analysis evaluation metrics using labeled dataset"""
    try:
        # Check if evaluation file exists
        csv_path = 'youtube_comments_cleaned.csv'
        
        if not os.path.exists(csv_path):
            return jsonify({
                'error': 'Dataset file not found. Please ensure youtube_comments_cleaned.csv exists.'
            }), 404
        
        # Load and sample dataset
        df = pd.read_csv(csv_path)
        df = df[df['CommentText'].str.strip().str.len() > 0]  # Remove empty
        
        # Sample for evaluation (limit to 1000 for performance)
        sample_size = min(1000, len(df))
        df_sample = df.sample(n=sample_size, random_state=42)
        
        # Helper function to analyze single comment
        def analyze_single_comment(text):
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            
            if polarity > 0.1:
                return 'Positive'
            elif polarity < -0.1:
                return 'Negative'
            else:
                return 'Neutral'
        
        # Apply TextBlob sentiment analysis
        df_sample['Predicted_Sentiment'] = df_sample['CommentText'].apply(analyze_single_comment)
        
        # Calculate metrics
        y_true = df_sample['Sentiment']
        y_pred = df_sample['Predicted_Sentiment']
        
        accuracy = accuracy_score(y_true, y_pred)
        precision, recall, f1, support = precision_recall_fscore_support(
            y_true, y_pred, labels=['Positive', 'Negative', 'Neutral'], zero_division=0, average=None
        )
        precision_macro, recall_macro, f1_macro, _ = precision_recall_fscore_support(
            y_true, y_pred, average='macro', zero_division=0
        )
        cm = confusion_matrix(y_true, y_pred, labels=['Positive', 'Negative', 'Neutral'])
        
        return jsonify({
            'dataset_info': {
                'total_comments': len(df),
                'evaluated_comments': sample_size,
                'sentiment_distribution': df_sample['Sentiment'].value_counts().to_dict()
            },
            'metrics': {
                'accuracy': round(accuracy, 4),
                'precision_macro': round(precision_macro, 4),
                'recall_macro': round(recall_macro, 4),
                'f1_macro': round(f1_macro, 4)
            },
            'per_class_metrics': {
                'positive': {
                    'precision': round(precision[0], 4),
                    'recall': round(recall[0], 4),
                    'f1_score': round(f1[0], 4),
                    'support': int(support[0])
                },
                'negative': {
                    'precision': round(precision[1], 4),
                    'recall': round(recall[1], 4),
                    'f1_score': round(f1[1], 4),
                    'support': int(support[1])
                },
                'neutral': {
                    'precision': round(precision[2], 4),
                    'recall': round(recall[2], 4),
                    'f1_score': round(f1[2], 4),
                    'support': int(support[2])
                }
            },
            'confusion_matrix': {
                'positive': {
                    'predicted_positive': int(cm[0][0]),
                    'predicted_negative': int(cm[0][1]),
                    'predicted_neutral': int(cm[0][2])
                },
                'negative': {
                    'predicted_positive': int(cm[1][0]),
                    'predicted_negative': int(cm[1][1]),
                    'predicted_neutral': int(cm[1][2])
                },
                'neutral': {
                    'predicted_positive': int(cm[2][0]),
                    'predicted_negative': int(cm[2][1]),
                    'predicted_neutral': int(cm[2][2])
                }
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Error calculating metrics: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
