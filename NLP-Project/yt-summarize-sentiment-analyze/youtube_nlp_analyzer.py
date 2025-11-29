#!/usr/bin/env python3
"""
YouTube Video NLP Analyzer
A Python application that extracts transcripts from YouTube videos,
performs summarization with adjustable temperature, and provides sentiment analysis.
"""

import os
import sys
import argparse
from typing import Optional, Dict, Any
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import re
from openai import OpenAI


class YouTubeNLPAnalyzer:
    """Main class for YouTube video analysis using NLP techniques."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """
        Initialize the analyzer with OpenAI API credentials.
        
        Args:
            api_key: OpenAI API key (if None, reads from OPENAI_API_KEY env var)
            model: The model to use for summarization (default: gpt-3.5-turbo)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            print("Warning: No OpenAI API key provided. Please set OPENAI_API_KEY environment variable.")
            print("You can still get transcripts, but summarization will not work.")
        
        self.model = model
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None
    
    @staticmethod
    def extract_video_id(url: str) -> str:
        """
        Extract YouTube video ID from various URL formats.
        
        Args:
            url: YouTube URL (supports multiple formats)
            
        Returns:
            Video ID string
            
        Raises:
            ValueError: If video ID cannot be extracted
        """
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)',
            r'youtube\.com\/embed\/([^&\n?#]+)',
            r'youtube\.com\/v\/([^&\n?#]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        raise ValueError(f"Could not extract video ID from URL: {url}")
    
    def get_transcript(self, video_url: str, language: str = 'en') -> str:
        """
        Fetch transcript from YouTube video.
        
        Args:
            video_url: YouTube video URL
            language: Preferred transcript language (default: 'en')
            
        Returns:
            Complete transcript as a single string
            
        Raises:
            Exception: If transcript cannot be fetched
        """
        try:
            video_id = self.extract_video_id(video_url)
            print(f"Fetching transcript for video ID: {video_id}")
            
            # Fetch transcript
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
            
            # Combine all text segments
            transcript_text = ' '.join([entry['text'] for entry in transcript_list])
            
            print(f"✓ Transcript fetched successfully ({len(transcript_text)} characters)")
            return transcript_text
            
        except TranscriptsDisabled:
            raise Exception("Transcripts are disabled for this video")
        except NoTranscriptFound:
            raise Exception(f"No transcript found in language: {language}")
        except Exception as e:
            raise Exception(f"Error fetching transcript: {str(e)}")
    
    def summarize(self, text: str, temperature: float = 0.7, max_tokens: int = 500) -> str:
        """
        Summarize text using OpenAI's GPT model.
        
        Args:
            text: Text to summarize
            temperature: Controls randomness (0.0-2.0). Lower is more focused, higher is more creative.
            max_tokens: Maximum length of the summary
            
        Returns:
            Summary text
            
        Raises:
            Exception: If API call fails or API key is missing
        """
        if not self.client:
            raise Exception("OpenAI API key not configured. Cannot perform summarization.")
        
        try:
            print(f"Generating summary with temperature={temperature}...")
            
            # Truncate text if too long (GPT-3.5-turbo has ~4096 token limit)
            max_input_chars = 12000  # Roughly 3000 tokens
            if len(text) > max_input_chars:
                print(f"Warning: Text truncated from {len(text)} to {max_input_chars} characters")
                text = text[:max_input_chars] + "..."
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that creates concise, informative summaries of video transcripts. Focus on the main points, key takeaways, and important details."},
                    {"role": "user", "content": f"Please provide a comprehensive summary of the following video transcript:\n\n{text}"}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            summary = response.choices[0].message.content.strip()
            print("✓ Summary generated successfully")
            return summary
            
        except Exception as e:
            raise Exception(f"Error during summarization: {str(e)}")
    
    def analyze_sentiment(self, text: str, temperature: float = 0.3) -> Dict[str, Any]:
        """
        Analyze sentiment of the text using OpenAI's GPT model.
        
        Args:
            text: Text to analyze
            temperature: Controls randomness (lower for more consistent results)
            
        Returns:
            Dictionary with sentiment analysis results
            
        Raises:
            Exception: If API call fails or API key is missing
        """
        if not self.client:
            raise Exception("OpenAI API key not configured. Cannot perform sentiment analysis.")
        
        try:
            print(f"Analyzing sentiment...")
            
            # Truncate text if too long
            max_input_chars = 12000
            if len(text) > max_input_chars:
                text = text[:max_input_chars] + "..."
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a sentiment analysis expert. Analyze the overall sentiment of the text and provide a classification (positive, negative, or neutral) along with a confidence score (0-100) and brief reasoning."},
                    {"role": "user", "content": f"Analyze the sentiment of this video transcript and respond in the following format:\nSentiment: [positive/negative/neutral]\nConfidence: [0-100]\nReasoning: [brief explanation]\n\nTranscript:\n{text}"}
                ],
                temperature=temperature,
                max_tokens=200
            )
            
            analysis = response.choices[0].message.content.strip()
            print("✓ Sentiment analysis completed")
            
            # Parse response
            result = {"raw_analysis": analysis}
            
            # Extract sentiment
            sentiment_match = re.search(r'Sentiment:\s*(\w+)', analysis, re.IGNORECASE)
            if sentiment_match:
                result['sentiment'] = sentiment_match.group(1).lower()
            
            # Extract confidence
            confidence_match = re.search(r'Confidence:\s*(\d+)', analysis, re.IGNORECASE)
            if confidence_match:
                result['confidence'] = int(confidence_match.group(1))
            
            return result
            
        except Exception as e:
            raise Exception(f"Error during sentiment analysis: {str(e)}")
    
    def full_analysis(self, video_url: str, temperature: float = 0.7, 
                     include_sentiment: bool = True) -> Dict[str, Any]:
        """
        Perform complete analysis: transcript extraction, summarization, and sentiment analysis.
        
        Args:
            video_url: YouTube video URL
            temperature: Temperature for text generation
            include_sentiment: Whether to include sentiment analysis
            
        Returns:
            Dictionary containing all analysis results
        """
        results = {}
        
        # Get transcript
        print("\n" + "="*60)
        print("STEP 1: Extracting Transcript")
        print("="*60)
        transcript = self.get_transcript(video_url)
        results['transcript'] = transcript
        results['transcript_length'] = len(transcript)
        
        # Summarize
        print("\n" + "="*60)
        print("STEP 2: Generating Summary")
        print("="*60)
        summary = self.summarize(transcript, temperature=temperature)
        results['summary'] = summary
        
        # Sentiment analysis
        if include_sentiment:
            print("\n" + "="*60)
            print("STEP 3: Analyzing Sentiment")
            print("="*60)
            sentiment = self.analyze_sentiment(transcript, temperature=0.3)
            results['sentiment'] = sentiment
        
        return results


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description='YouTube Video NLP Analyzer - Extract transcripts, summarize, and analyze sentiment',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage - get transcript and summary
  python youtube_nlp_analyzer.py https://www.youtube.com/watch?v=VIDEO_ID
  
  # Adjust temperature for more creative summaries
  python youtube_nlp_analyzer.py https://www.youtube.com/watch?v=VIDEO_ID --temperature 1.2
  
  # Get only transcript (no API calls)
  python youtube_nlp_analyzer.py https://www.youtube.com/watch?v=VIDEO_ID --transcript-only
  
  # Full analysis with sentiment
  python youtube_nlp_analyzer.py https://www.youtube.com/watch?v=VIDEO_ID --sentiment
        """
    )
    
    parser.add_argument('url', help='YouTube video URL')
    parser.add_argument('-t', '--temperature', type=float, default=0.7,
                       help='Temperature for text generation (0.0-2.0). Default: 0.7')
    parser.add_argument('-m', '--model', default='gpt-3.5-turbo',
                       help='OpenAI model to use. Default: gpt-3.5-turbo')
    parser.add_argument('--max-tokens', type=int, default=500,
                       help='Maximum tokens for summary. Default: 500')
    parser.add_argument('--transcript-only', action='store_true',
                       help='Only extract transcript (skip summarization)')
    parser.add_argument('--sentiment', action='store_true',
                       help='Include sentiment analysis')
    parser.add_argument('-l', '--language', default='en',
                       help='Transcript language code. Default: en')
    
    args = parser.parse_args()
    
    # Validate temperature
    if not 0.0 <= args.temperature <= 2.0:
        print("Error: Temperature must be between 0.0 and 2.0")
        sys.exit(1)
    
    # Initialize analyzer
    analyzer = YouTubeNLPAnalyzer(model=args.model)
    
    try:
        if args.transcript_only:
            # Only get transcript
            print("\n" + "="*60)
            print("Extracting Transcript")
            print("="*60)
            transcript = analyzer.get_transcript(args.url, language=args.language)
            print("\n" + "="*60)
            print("TRANSCRIPT")
            print("="*60)
            print(transcript)
        else:
            # Full analysis
            results = analyzer.full_analysis(
                args.url, 
                temperature=args.temperature,
                include_sentiment=args.sentiment
            )
            
            # Display results
            print("\n" + "="*60)
            print("RESULTS")
            print("="*60)
            print(f"\n📊 Transcript Length: {results['transcript_length']} characters\n")
            
            print("📝 TRANSCRIPT:")
            print("-" * 60)
            print(results['transcript'][:500] + "..." if len(results['transcript']) > 500 else results['transcript'])
            print()
            
            print("📋 SUMMARY:")
            print("-" * 60)
            print(results['summary'])
            print()
            
            if 'sentiment' in results:
                print("💭 SENTIMENT ANALYSIS:")
                print("-" * 60)
                sentiment_data = results['sentiment']
                if 'sentiment' in sentiment_data:
                    print(f"Sentiment: {sentiment_data['sentiment'].upper()}")
                if 'confidence' in sentiment_data:
                    print(f"Confidence: {sentiment_data['confidence']}%")
                print(f"\n{sentiment_data['raw_analysis']}")
            
            print("\n" + "="*60)
            print(f"Analysis completed with temperature={args.temperature}")
            print("="*60)
    
    except Exception as e:
        print(f"\n❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
