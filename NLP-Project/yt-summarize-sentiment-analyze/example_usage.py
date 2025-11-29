#!/usr/bin/env python3
"""
Example usage demonstrations for YouTube NLP Analyzer.
This script shows various ways to use the YouTubeNLPAnalyzer class.
"""

from youtube_nlp_analyzer import YouTubeNLPAnalyzer
import os


def example_1_basic_usage():
    """Example 1: Basic transcript extraction and summarization."""
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Usage - Transcript and Summary")
    print("="*70)
    
    # Initialize analyzer
    analyzer = YouTubeNLPAnalyzer()
    
    # Example video URL (replace with any YouTube URL)
    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    try:
        # Get transcript
        transcript = analyzer.get_transcript(video_url)
        print(f"\n✓ Transcript extracted ({len(transcript)} characters)")
        print(f"Preview: {transcript[:200]}...")
        
        # Generate summary
        summary = analyzer.summarize(transcript)
        print(f"\n✓ Summary:\n{summary}")
        
    except Exception as e:
        print(f"Error: {e}")


def example_2_temperature_variations():
    """Example 2: Experimenting with different temperature values."""
    print("\n" + "="*70)
    print("EXAMPLE 2: Temperature Variations")
    print("="*70)
    
    analyzer = YouTubeNLPAnalyzer()
    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    # Test different temperatures
    temperatures = [0.3, 0.7, 1.2]
    
    try:
        transcript = analyzer.get_transcript(video_url)
        
        for temp in temperatures:
            print(f"\n--- Temperature = {temp} ---")
            summary = analyzer.summarize(transcript, temperature=temp, max_tokens=200)
            print(summary)
            print()
        
    except Exception as e:
        print(f"Error: {e}")


def example_3_full_analysis():
    """Example 3: Complete analysis including sentiment."""
    print("\n" + "="*70)
    print("EXAMPLE 3: Full Analysis (Transcript + Summary + Sentiment)")
    print("="*70)
    
    analyzer = YouTubeNLPAnalyzer()
    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    try:
        results = analyzer.full_analysis(video_url, temperature=0.7, include_sentiment=True)
        
        print(f"\n📊 Transcript Length: {results['transcript_length']} characters")
        
        print("\n📝 Summary:")
        print(results['summary'])
        
        if 'sentiment' in results:
            print("\n💭 Sentiment Analysis:")
            sentiment_data = results['sentiment']
            if 'sentiment' in sentiment_data:
                print(f"  Sentiment: {sentiment_data['sentiment'].upper()}")
            if 'confidence' in sentiment_data:
                print(f"  Confidence: {sentiment_data['confidence']}%")
        
    except Exception as e:
        print(f"Error: {e}")


def example_4_transcript_only():
    """Example 4: Extract transcript without API calls."""
    print("\n" + "="*70)
    print("EXAMPLE 4: Transcript Only (No API Required)")
    print("="*70)
    
    analyzer = YouTubeNLPAnalyzer()  # No API key needed for transcript only
    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    try:
        transcript = analyzer.get_transcript(video_url)
        print(f"\n✓ Transcript extracted successfully!")
        print(f"Length: {len(transcript)} characters")
        print(f"Word count: ~{len(transcript.split())} words")
        print(f"\nFirst 500 characters:\n{transcript[:500]}...")
        
    except Exception as e:
        print(f"Error: {e}")


def example_5_different_models():
    """Example 5: Using different OpenAI models."""
    print("\n" + "="*70)
    print("EXAMPLE 5: Comparing Different Models")
    print("="*70)
    
    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    models = ["gpt-3.5-turbo", "gpt-4"]  # Add gpt-4 if you have access
    
    try:
        for model in models:
            print(f"\n--- Using {model} ---")
            analyzer = YouTubeNLPAnalyzer(model=model)
            
            transcript = analyzer.get_transcript(video_url)
            summary = analyzer.summarize(transcript, temperature=0.7, max_tokens=300)
            
            print(summary)
            
    except Exception as e:
        print(f"Error: {e}")


def example_6_batch_processing():
    """Example 6: Analyzing multiple videos."""
    print("\n" + "="*70)
    print("EXAMPLE 6: Batch Processing Multiple Videos")
    print("="*70)
    
    analyzer = YouTubeNLPAnalyzer()
    
    # List of video URLs to analyze
    video_urls = [
        "https://www.youtube.com/watch?v=VIDEO_ID_1",
        "https://www.youtube.com/watch?v=VIDEO_ID_2",
        "https://www.youtube.com/watch?v=VIDEO_ID_3",
    ]
    
    results_list = []
    
    for i, url in enumerate(video_urls, 1):
        print(f"\n--- Processing Video {i}/{len(video_urls)} ---")
        try:
            results = analyzer.full_analysis(url, temperature=0.7, include_sentiment=False)
            results_list.append({
                'url': url,
                'summary': results['summary'],
                'length': results['transcript_length']
            })
            print(f"✓ Video {i} processed successfully")
            
        except Exception as e:
            print(f"✗ Error with video {i}: {e}")
    
    # Display all results
    print("\n" + "="*70)
    print("BATCH RESULTS SUMMARY")
    print("="*70)
    for i, result in enumerate(results_list, 1):
        print(f"\nVideo {i}:")
        print(f"Length: {result['length']} characters")
        print(f"Summary: {result['summary'][:150]}...")


def main():
    """Run example demonstrations."""
    print("\n" + "="*70)
    print("YouTube NLP Analyzer - Example Usage Demonstrations")
    print("="*70)
    
    # Check if API key is set
    if not os.getenv('OPENAI_API_KEY'):
        print("\n⚠️  WARNING: OPENAI_API_KEY not found in environment variables.")
        print("Some examples require an API key. Set it in .env file.")
        print("You can still run Example 4 (transcript only) without an API key.\n")
    
    print("\nAvailable examples:")
    print("1. Basic Usage - Transcript and Summary")
    print("2. Temperature Variations")
    print("3. Full Analysis (with Sentiment)")
    print("4. Transcript Only (No API required)")
    print("5. Comparing Different Models")
    print("6. Batch Processing Multiple Videos")
    print("\nNote: Replace example URLs with real YouTube video URLs")
    
    # Uncomment to run specific examples:
    
    # example_1_basic_usage()
    # example_2_temperature_variations()
    # example_3_full_analysis()
    # example_4_transcript_only()
    # example_5_different_models()
    # example_6_batch_processing()
    
    print("\n" + "="*70)
    print("To run examples, uncomment the function calls in main()")
    print("="*70)


if __name__ == "__main__":
    main()
