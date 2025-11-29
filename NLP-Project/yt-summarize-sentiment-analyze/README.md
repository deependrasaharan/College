# YouTube NLP Analyzer 🎥📊

A comprehensive Python application that leverages Large Language Models (LLMs) to analyze YouTube videos. This project extracts video transcripts, generates intelligent summaries, and performs sentiment analysis using state-of-the-art NLP techniques.

## 🎯 Features

- **Transcript Extraction**: Automatically fetch transcripts from any YouTube video
- **AI-Powered Summarization**: Generate concise, informative summaries using OpenAI's GPT models
- **Temperature Control**: Adjust the creativity/randomness of generated summaries (0.0 = focused, 2.0 = creative)
- **Sentiment Analysis**: Determine the overall sentiment (positive, negative, neutral) of video content
- **CLI Interface**: Easy-to-use command-line interface with multiple options
- **Flexible Configuration**: Environment-based configuration for easy customization

## 📋 Requirements

- Python 3.8 or higher
- OpenAI API key (for summarization and sentiment analysis)
- Internet connection (for YouTube transcript fetching and API calls)

## 🚀 Installation

### 1. Clone or download this project

```bash
cd yt-summarize-sentiment-analyze
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv

# On Linux/Mac
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your OpenAI API key

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL=gpt-3.5-turbo
DEFAULT_TEMPERATURE=0.7
```

**Get your API key**: https://platform.openai.com/api-keys

## 📖 Usage

### Basic Usage

Extract transcript and generate summary:

```bash
python youtube_nlp_analyzer.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Advanced Options

**Adjust temperature** (0.0 = focused, 2.0 = creative):

```bash
python youtube_nlp_analyzer.py "https://www.youtube.com/watch?v=VIDEO_ID" --temperature 1.2
```

**Include sentiment analysis**:

```bash
python youtube_nlp_analyzer.py "https://www.youtube.com/watch?v=VIDEO_ID" --sentiment
```

**Get transcript only** (no API calls needed):

```bash
python youtube_nlp_analyzer.py "https://www.youtube.com/watch?v=VIDEO_ID" --transcript-only
```

**Change transcript language**:

```bash
python youtube_nlp_analyzer.py "https://www.youtube.com/watch?v=VIDEO_ID" --language es
```

**Use different model**:

```bash
python youtube_nlp_analyzer.py "https://www.youtube.com/watch?v=VIDEO_ID" --model gpt-4
```

**Adjust summary length**:

```bash
python youtube_nlp_analyzer.py "https://www.youtube.com/watch?v=VIDEO_ID" --max-tokens 1000
```

### Complete Example

```bash
python youtube_nlp_analyzer.py \
  "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  --temperature 0.8 \
  --sentiment \
  --max-tokens 750 \
  --model gpt-3.5-turbo
```

## 🎛️ Temperature Parameter Explained

The **temperature** parameter controls the randomness/creativity of the AI's responses:

| Temperature | Behavior | Use Case |
|-------------|----------|----------|
| 0.0 - 0.3 | Very focused, deterministic | Technical content, precise summaries |
| 0.4 - 0.7 | Balanced (default: 0.7) | General use, most videos |
| 0.8 - 1.2 | More creative, varied | Entertainment, creative content |
| 1.3 - 2.0 | Very creative, unpredictable | Experimental, artistic interpretations |

## 📂 Project Structure

```
yt-summarize-sentiment-analyze/
├── youtube_nlp_analyzer.py    # Main application script
├── config.py                  # Configuration management
├── requirements.txt           # Python dependencies
├── example_usage.py           # Example usage demonstrations
├── .env.example              # Environment variable template
├── .gitignore                # Git ignore rules
├── README.md                 # This file
├── project-description.txt   # Project requirements
└── project-guidelines.txt    # Academic guidelines
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```bash
# Required
OPENAI_API_KEY=your-api-key-here

# Optional (with defaults)
OPENAI_MODEL=gpt-3.5-turbo
DEFAULT_TEMPERATURE=0.7
DEFAULT_MAX_TOKENS=500
DEFAULT_LANGUAGE=en
```

### Programmatic Usage

You can also use the analyzer in your own Python scripts:

```python
from youtube_nlp_analyzer import YouTubeNLPAnalyzer

# Initialize
analyzer = YouTubeNLPAnalyzer(api_key="your-key", model="gpt-3.5-turbo")

# Get transcript only
transcript = analyzer.get_transcript("https://www.youtube.com/watch?v=VIDEO_ID")

# Summarize with custom temperature
summary = analyzer.summarize(transcript, temperature=0.9)

# Full analysis
results = analyzer.full_analysis(
    "https://www.youtube.com/watch?v=VIDEO_ID",
    temperature=0.7,
    include_sentiment=True
)

print(results['summary'])
print(results['sentiment'])
```

## 🎓 Academic Context

This project fulfills the requirements for an NLP course project focused on:

- **LLM Integration**: Leveraging state-of-the-art language models (GPT-3.5/4) for real-world applications
- **Text Summarization**: Implementing abstractive summarization using transformer-based models
- **Sentiment Analysis**: Applying NLP techniques to understand emotional content
- **Practical Application**: Solving real problems (analyzing video content at scale)

### Key NLP Concepts Demonstrated

1. **Text Preprocessing**: Handling raw transcript data, text cleaning
2. **API Integration**: Working with modern LLM APIs (OpenAI)
3. **Prompt Engineering**: Crafting effective prompts for summarization and analysis
4. **Parameter Tuning**: Understanding temperature and its effects on generation
5. **Multi-task Learning**: Combining multiple NLP tasks (summarization + sentiment analysis)

## 📊 Evaluation Metrics

For academic evaluation, this project can be assessed using:

- **ROUGE scores**: For summarization quality (comparing with human summaries)
- **Accuracy/F1**: For sentiment classification (with labeled data)
- **Qualitative assessment**: Coherence, relevance, and informativeness of summaries
- **User feedback**: Practical utility of the tool

## ⚠️ Limitations

- Requires transcripts to be available on YouTube (not all videos have them)
- API costs for OpenAI (though minimal for most use cases)
- Text truncation for very long videos (due to token limits)
- Language support depends on available YouTube transcripts

## 🔍 Troubleshooting

### "No transcript found"
- Not all videos have transcripts. Try videos with captions/subtitles enabled.
- Try different language codes: `--language en`, `--language es`, etc.

### "API key not configured"
- Ensure your `.env` file exists and contains `OPENAI_API_KEY=your-key`
- Verify the API key is valid at https://platform.openai.com/api-keys

### "Rate limit exceeded"
- You've hit OpenAI's rate limits. Wait a moment and try again.
- Consider upgrading your OpenAI plan for higher limits.

### Import errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Activate your virtual environment if using one.

## 🤝 Contributing

This is an academic project, but improvements are welcome:

1. Add support for more video platforms
2. Implement offline summarization using open-source models
3. Add support for multiple transcript languages in analysis
4. Create a web interface (Flask/FastAPI)
5. Add more advanced sentiment metrics

## 📝 License

This project is created for educational purposes as part of an NLP course project.

## 🙏 Acknowledgments

- **OpenAI**: For providing powerful LLM APIs
- **youtube-transcript-api**: For easy transcript extraction
- Course instructors and guidelines for project direction

## 📧 Support

For issues, questions, or suggestions, please refer to the project documentation or contact the course instructor.

---

**Note**: Remember to never commit your `.env` file with actual API keys to version control!
