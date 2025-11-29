"""
System Architecture Diagram for YouTube NLP Analyzer

ASCII Diagram showing the complete system flow and components
"""

SYSTEM_ARCHITECTURE = """
╔══════════════════════════════════════════════════════════════════════════╗
║                     YOUTUBE NLP ANALYZER ARCHITECTURE                    ║
╚══════════════════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────────────────────┐
│                              USER INTERFACE                              │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────────┐              ┌─────────────────────┐          │
│  │   CLI Interface     │              │  Python API         │          │
│  │  (argparse)         │              │  (Programmatic)     │          │
│  │                     │              │                     │          │
│  │  • --temperature    │              │  analyzer =         │          │
│  │  • --sentiment      │              │    YouTubeNLP...()  │          │
│  │  • --transcript-only│              │  analyzer.          │          │
│  │  • --help           │              │    full_analysis()  │          │
│  └─────────┬───────────┘              └──────────┬──────────┘          │
│            │                                     │                      │
└────────────┼─────────────────────────────────────┼──────────────────────┘
             │                                     │
             └───────────────┬─────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                          CORE APPLICATION                                │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│                    ┌──────────────────────────┐                         │
│                    │ YouTubeNLPAnalyzer Class│                         │
│                    └────────────┬─────────────┘                         │
│                                 │                                        │
│          ┌──────────────────────┼──────────────────────┐               │
│          │                      │                      │               │
│          ▼                      ▼                      ▼               │
│  ┌───────────────┐    ┌────────────────┐    ┌────────────────┐       │
│  │   Extract     │    │   Summarize    │    │    Analyze     │       │
│  │   Video ID    │    │     Text       │    │   Sentiment    │       │
│  └───────┬───────┘    └────────┬───────┘    └────────┬───────┘       │
│          │                     │                      │               │
│          │  URL Parsing        │  GPT API Call        │  GPT API Call  │
│          │  (Regex)            │  (Temperature)       │  (Low Temp)    │
│          │                     │                      │               │
└──────────┼─────────────────────┼──────────────────────┼───────────────┘
           │                     │                      │
           ▼                     ▼                      ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                          EXTERNAL SERVICES                               │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────────────┐              ┌──────────────────────┐        │
│  │   YouTube            │              │   OpenAI GPT API     │        │
│  │   Transcript API     │              │   (GPT-3.5/GPT-4)    │        │
│  │                      │              │                      │        │
│  │  • Fetch transcripts │              │  • Summarization     │        │
│  │  • Multi-language    │              │  • Sentiment analysis│        │
│  │  • Free service      │              │  • Temperature param │        │
│  └──────────────────────┘              └──────────────────────┘        │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│                           DATA FLOW DIAGRAM                              │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────┐                                                           │
│  │ YouTube  │                                                           │
│  │   URL    │                                                           │
│  └────┬─────┘                                                           │
│       │                                                                  │
│       ▼                                                                  │
│  ┌─────────────────┐      ┌──────────────────┐                         │
│  │ Extract Video ID│─────▶│  Fetch Transcript│                         │
│  └─────────────────┘      └────────┬─────────┘                         │
│                                     │                                    │
│                            ┌────────▼──────────┐                        │
│                            │  Raw Transcript   │                        │
│                            │  (Plain Text)     │                        │
│                            └────────┬──────────┘                        │
│                                     │                                    │
│                       ┌─────────────┼─────────────┐                     │
│                       │                           │                     │
│                       ▼                           ▼                     │
│          ┌────────────────────┐     ┌────────────────────┐            │
│          │   Summarization    │     │ Sentiment Analysis │            │
│          │   (GPT + Temp)     │     │   (GPT Low Temp)   │            │
│          └─────────┬──────────┘     └─────────┬──────────┘            │
│                    │                           │                        │
│                    ▼                           ▼                        │
│          ┌────────────────┐         ┌──────────────────┐              │
│          │ Summary Text   │         │ Sentiment Result │              │
│          │ (Abstractive)  │         │ (Classification) │              │
│          └────────┬───────┘         └──────────┬───────┘              │
│                   │                            │                        │
│                   └────────────┬───────────────┘                        │
│                                │                                        │
│                                ▼                                        │
│                   ┌────────────────────────┐                           │
│                   │   Combined Results     │                           │
│                   │   (Display to User)    │                           │
│                   └────────────────────────┘                           │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│                         CONFIGURATION LAYER                              │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────┐        ┌──────────────┐        ┌──────────────┐     │
│  │   .env       │───────▶│  config.py   │───────▶│ Application  │     │
│  │   File       │        │   Module     │        │   Settings   │     │
│  └──────────────┘        └──────────────┘        └──────────────┘     │
│                                                                          │
│  Environment Variables:                                                 │
│  • OPENAI_API_KEY         → Required for LLM operations                │
│  • OPENAI_MODEL           → Model selection (default: gpt-3.5-turbo)   │
│  • DEFAULT_TEMPERATURE    → Default creativity level (0.7)             │
│  • DEFAULT_MAX_TOKENS     → Max summary length (500)                   │
│  • DEFAULT_LANGUAGE       → Transcript language (en)                   │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│                         MODULE DEPENDENCIES                              │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  youtube_nlp_analyzer.py                                                │
│  ├── youtube-transcript-api  (Transcript extraction)                    │
│  ├── openai                  (GPT API client)                           │
│  ├── python-dotenv           (Environment variables)                    │
│  └── Standard library        (re, os, sys, argparse, typing)           │
│                                                                          │
│  config.py                                                              │
│  ├── python-dotenv           (Load .env file)                           │
│  └── Standard library        (os, typing)                               │
│                                                                          │
│  example_usage.py                                                       │
│  └── youtube_nlp_analyzer    (Import main class)                        │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│                    CLASS STRUCTURE & METHODS                             │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  class YouTubeNLPAnalyzer:                                              │
│                                                                          │
│      __init__(api_key, model)                                           │
│      │   Initialize with API credentials and model selection            │
│      │                                                                   │
│      ├── extract_video_id(url) → str                                    │
│      │   Parse YouTube URL and extract video ID                         │
│      │                                                                   │
│      ├── get_transcript(video_url, language) → str                      │
│      │   Fetch transcript from YouTube Transcript API                   │
│      │                                                                   │
│      ├── summarize(text, temperature, max_tokens) → str                 │
│      │   Generate summary using GPT with adjustable temperature         │
│      │                                                                   │
│      ├── analyze_sentiment(text, temperature) → Dict                    │
│      │   Analyze sentiment with classification and confidence           │
│      │                                                                   │
│      └── full_analysis(video_url, temp, sentiment) → Dict               │
│          Complete pipeline: transcript → summary → sentiment            │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│                      ERROR HANDLING STRATEGY                             │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Try-Except Blocks:                                                     │
│  ├── TranscriptsDisabled    → "Transcripts disabled for this video"    │
│  ├── NoTranscriptFound      → "No transcript in specified language"    │
│  ├── ValueError             → "Invalid URL or parameters"               │
│  ├── API Errors             → "OpenAI API error: [details]"            │
│  └── Generic Exception      → "Unexpected error: [details]"            │
│                                                                          │
│  Validation:                                                            │
│  ├── Temperature range      → Must be 0.0 to 2.0                       │
│  ├── API key presence       → Warning if not configured                │
│  ├── URL format             → Multiple regex patterns for flexibility  │
│  └── Text length            → Truncation for token limits              │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│                      PERFORMANCE OPTIMIZATION                            │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Text Processing:                                                       │
│  • Truncation at 12,000 chars (~3,000 tokens)                          │
│  • Efficient string concatenation                                       │
│  • Single-pass transcript joining                                       │
│                                                                          │
│  API Efficiency:                                                        │
│  • Reuse OpenAI client instance                                         │
│  • Configurable max_tokens to limit cost                               │
│  • Lower temperature for sentiment (faster, cheaper)                    │
│                                                                          │
│  Resource Management:                                                   │
│  • No file I/O (all in-memory)                                          │
│  • Minimal dependencies                                                 │
│  • Lazy loading of heavy libraries                                      │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘

End of Architecture Documentation
"""

if __name__ == "__main__":
    print(SYSTEM_ARCHITECTURE)
