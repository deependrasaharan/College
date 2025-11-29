# Quick Start Guide

## Step-by-Step Setup

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Your API Key

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```bash
OPENAI_API_KEY=sk-your-actual-api-key-here
```

**Get an API key**: Visit https://platform.openai.com/api-keys

### 3. Test the Installation

Try getting a transcript (no API key needed):
```bash
python youtube_nlp_analyzer.py "https://www.youtube.com/watch?v=VIDEO_ID" --transcript-only
```

### 4. Run Your First Analysis

```bash
python youtube_nlp_analyzer.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

## Common Commands

### Get help
```bash
python youtube_nlp_analyzer.py --help
```

### Basic summarization
```bash
python youtube_nlp_analyzer.py "YOUTUBE_URL"
```

### With sentiment analysis
```bash
python youtube_nlp_analyzer.py "YOUTUBE_URL" --sentiment
```

### Adjust temperature (creativity)
```bash
python youtube_nlp_analyzer.py "YOUTUBE_URL" --temperature 1.0
```

### Transcript only (no API needed)
```bash
python youtube_nlp_analyzer.py "YOUTUBE_URL" --transcript-only
```

## Troubleshooting

### "No module named 'youtube_transcript_api'"
Run: `pip install -r requirements.txt`

### "OPENAI_API_KEY not configured"
1. Create a `.env` file from `.env.example`
2. Add your API key: `OPENAI_API_KEY=your-key`

### "No transcript found"
- Not all YouTube videos have transcripts
- Try videos with captions/subtitles enabled
- Try different language: `--language en`

## Example Video URLs (for testing)

Replace VIDEO_ID with actual YouTube video IDs:
- Educational: Search for TED talks, tutorials
- News: Search for news channels
- Entertainment: Search for vlogs, reviews

## Next Steps

1. Check `README.md` for full documentation
2. See `example_usage.py` for code examples
3. Experiment with different temperature values
4. Try sentiment analysis on different video types

## Cost Considerations

- Getting transcripts: FREE
- GPT-3.5-turbo summarization: ~$0.0005-0.002 per video
- GPT-4 summarization: ~$0.01-0.03 per video

Most educational/testing usage will cost less than $1.
