# 🎥 YouTube Video Summarizer with NLP Evaluation

A comprehensive web-based tool that extracts transcripts from YouTube videos, generates AI-powered summaries using Google's Gemini API, and provides academic-grade evaluation metrics for model comparison.

## Features

### Core Features
- 📝 **Extract Transcripts**: Automatically fetch transcripts with dual fallback system (youtube-transcript-api + yt-dlp)
- 🤖 **AI Summarization**: Generate comprehensive summaries using Gemini AI
- 🎚️ **Temperature Control**: Adjust the creativity level of AI responses (0.0 - 1.0)
- 📏 **Length Options**: Choose between concise, medium, or detailed summaries
- 🌐 **Web Interface**: Professional, modern UI with custom color palette
- 📋 **Copy to Clipboard**: Easy copy functionality for transcripts and summaries
- 🎬 **Video Preview**: Embedded video player for reference

### Advanced Features (Academic)
- 🔤 **NLP Preprocessing**: Optional tokenization, stop-word removal, and text normalization (NLTK)
- 💬 **Sentiment Analysis**: Analyze YouTube comments with TextBlob (positive/negative/neutral classification)
- 📊 **Sentiment Evaluation**: Measure accuracy, precision, recall, F1-score against 1M+ labeled dataset
- 🔬 **Multi-Model Evaluation**: Compare 3 different Gemini models side-by-side
- 📊 **ROUGE Metrics**: Industry-standard evaluation (ROUGE-1, ROUGE-2, ROUGE-L)
- ⏱️ **Performance Metrics**: Processing time, compression ratio, word counts
- 📈 **Visual Dashboard**: Comprehensive metrics display with color-coded indicators

## Prerequisites

- Python 3.7 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))
- YouTube Data API key ([Get one here](https://console.cloud.google.com/apis/credentials)) - Optional, for comment analysis

## Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd yt-tool
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # On Linux/Mac:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Download NLTK data** (required for preprocessing):
   ```bash
   python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('stopwords'); nltk.download('brown')"
   ```

5. **Set up your API keys**:
   - Copy the `.env.example` file to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Open `.env` and add your API keys:
     ```
     GEMINI_API_KEY=your_gemini_api_key_here
     YOUTUBE_API_KEY=your_youtube_api_key_here  # Optional, for comment analysis
     ```

## Usage

### Basic Summarization

1. **Start the application**:
   ```bash
   python app.py
   ```

2. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

3. **Analyze a video**:
   - Paste a YouTube URL into the input field
   - Select summary length (concise/medium/detailed)
   - Adjust temperature slider (0.0 = focused, 1.0 = creative)
   - Optional: Check "Analyze comments & sentiment"
   - Optional: Check "Apply NLP preprocessing"
   - Click "Analyze Video"
   - View the summary, transcript, and sentiment analysis

### Advanced: Multi-Model Evaluation

1. **Follow steps 1-2 above**

2. **Run evaluation**:
   - Enter a YouTube URL
   - Configure your preferred settings
   - Click "Evaluate Multiple Models"
   - Wait 30-60 seconds for comprehensive analysis

3. **Review results**:
   - Compare 3 different Gemini models
   - Analyze ROUGE scores (ROUGE-1, ROUGE-2, ROUGE-L)
   - Check processing times
   - Review compression ratios
   - Read generated summaries side-by-side

### Sentiment Analysis Evaluation

1. **View metrics**:
   - Click "Show Sentiment Analysis Metrics" button
   - See accuracy, precision, recall, F1-scores
   - Review confusion matrix
   - Analyze per-class performance

2. **Dataset**: 1M+ labeled YouTube comments
3. **Results**: ~49% accuracy with TextBlob (documented in SENTIMENT_EVALUATION.md)

## Configuration Options

### Temperature Guide
The temperature parameter controls the randomness and creativity of AI responses:
- **0.0 - 0.3**: More focused and deterministic responses
- **0.4 - 0.7**: Balanced creativity and coherence (recommended)
- **0.8 - 1.0**: More creative and varied responses

### Summary Length Options
- **Concise**: 2-3 sentence brief summary
- **Medium**: Balanced summary with main points (default)
- **Detailed**: Comprehensive summary with all details

### NLP Preprocessing
When enabled, applies:
- **Tokenization**: Splits text into words
- **Stop-word Removal**: Removes common words (the, is, at, etc.)
- **Text Normalization**: Lowercase + punctuation removal

### Models Evaluated
- **gemini-2.0-flash-exp**: Latest experimental model
- **gemini-2.5-flash**: Fast, efficient summarization
- **gemini-2.5-pro**: Higher quality, detailed summaries

## Project Structure

```
yt-tool/
├── app.py                          # Main Flask application with all routes
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── .env                            # Your API keys (create this file)
├── .gitignore                      # Git ignore rules
├── README.md                       # This file
├── PHASE1_IMPLEMENTATION.md        # Phase 1 preprocessing documentation
├── EVALUATION_FEATURES.md          # Multi-model evaluation documentation
├── SENTIMENT_EVALUATION.md         # Sentiment analysis metrics & results
├── MODEL_FIX.md                    # Model compatibility notes
├── project-description.txt         # Original project requirements
├── project-guidelines.txt          # Academic requirements
├── youtube_comments_cleaned.csv    # 1M+ labeled comments dataset
├── evaluate_sentiment.py           # Standalone sentiment evaluation script
└── templates/
    └── index.html                  # Web interface with evaluation UI
```

## How It Works

### Basic Flow
1. **URL Processing**: Extracts video ID from various YouTube URL formats
2. **Transcript Fetching**: Uses youtube-transcript-api (primary) and yt-dlp (fallback)
3. **Optional Preprocessing**: Applies NLP preprocessing if enabled
4. **AI Summarization**: Sends processed transcript to Gemini API
5. **Results Display**: Shows summary, transcript, and optional sentiment analysis

### Evaluation Flow
1. **Transcript Extraction**: Same as basic flow
2. **Multi-Model Processing**: Tests 3 Gemini models sequentially
3. **Metrics Calculation**: Computes ROUGE scores, timing, compression
4. **Comparison Dashboard**: Displays side-by-side results with metrics

### ROUGE Metrics
- **ROUGE-1**: Unigram (single word) overlap
- **ROUGE-2**: Bigram (word pair) overlap
- **ROUGE-L**: Longest common subsequence
- Each provides: Precision, Recall, F-measure

## Troubleshooting

### Transcript Issues
**"Transcripts are disabled for this video"**
- The video owner has disabled transcripts/captions
- Try a different video

**"No transcript found for this video"**
- The video doesn't have auto-generated or manual captions
- System automatically tries yt-dlp fallback

### API Issues
**"GEMINI_API_KEY not found"**
- Make sure you created a `.env` file (not `.env.example`)
- Verify your API key is correctly set
- Restart the application after adding the key

**Comment analysis not working**
- Requires YOUTUBE_API_KEY in .env
- Enable YouTube Data API v3 in Google Cloud Console
- Check API quota limits

### Evaluation Issues
**"Model not found" errors during evaluation**
- Some models may not be available in your region
- Skip failed models, evaluation continues
- Check Gemini API model availability

**Evaluation takes too long**
- Normal: 30-60 seconds for 3 models
- Depends on transcript length and network speed
- Consider using shorter videos for testing

### Installation Issues
**Import errors**
- Install all dependencies: `pip install -r requirements.txt`
- Download NLTK data as shown in installation steps
- Verify Python 3.7+: `python --version`

**NLTK download errors**
- Run NLTK download commands individually
- Check internet connection
- Ensure write permissions to nltk_data directory

## Dependencies

### Core Dependencies
- **Flask**: Web framework
- **youtube-transcript-api**: Primary transcript fetching
- **yt-dlp**: Fallback transcript extraction
- **google-generativeai**: Google Gemini API client
- **google-api-python-client**: YouTube Data API (for comments)
- **python-dotenv**: Environment variable management

### NLP/Analysis Dependencies
- **textblob**: Sentiment analysis (no API key needed)
- **nltk**: Natural Language Toolkit for preprocessing
- **rouge-score**: ROUGE metrics for evaluation

## Notes

- Works with videos that have transcripts/captions available
- Processing time depends on video length and API response time
- API rate limits apply based on your Gemini API tier
- Comment analysis limited to 100 top comments per video
- ROUGE scores computed against first 1000 words of transcript
- Evaluation makes 3 sequential API calls (one per model)
- Preprocessing may improve or reduce summary quality depending on content
- Best results with videos 5-30 minutes long

## Academic Features

This tool was developed to meet academic requirements including:
- ✅ Phase 1: NLP preprocessing pipeline (tokenization, stop-words, normalization)
- ✅ Phase 2: Multi-model comparison framework
- ✅ Phase 3: Evaluation metrics (ROUGE, processing time, compression)
- ✅ Phase 4: Visual metrics dashboard

See `PHASE1_IMPLEMENTATION.md` and `EVALUATION_FEATURES.md` for detailed documentation.

## Performance Tips

1. **For Faster Results**: Use "concise" length with gemini-2.0-flash-exp
2. **For Best Quality**: Use "detailed" length with gemini-1.5-pro
3. **For Testing**: Start with short videos (5-10 minutes)
4. **For Academic Evaluation**: Use medium-length videos with clear topic structure

## License

This project is for educational purposes.
