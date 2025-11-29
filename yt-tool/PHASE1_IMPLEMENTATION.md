# Phase 1 Implementation: NLP Preprocessing Pipeline

## Overview
Phase 1 implements the core NLP preprocessing pipeline as required by `project-guidelines.txt`. This phase adds optional text preprocessing before summarization.

## Features Implemented

### 1. Tokenization
- Uses NLTK's `word_tokenize()` to split text into individual tokens
- Handles punctuation and special characters properly
- Preserves word boundaries while removing noise

### 2. Stop-Word Removal
- Removes common English stop words using NLTK's stopwords corpus
- Filters out words like "the", "is", "at", "which", "on", etc.
- Reduces transcript length while preserving semantic meaning

### 3. Text Normalization
- Converts all text to lowercase for consistency
- Removes punctuation marks using Python's string.punctuation
- Filters out empty tokens and extra whitespace

### 4. Optional Application
- Added checkbox in UI: "Apply NLP preprocessing"
- Preprocessing is **optional** and disabled by default
- Can compare results with/without preprocessing

## Technical Implementation

### Backend Changes (`app.py`)

```python
def preprocess_text(text, apply_preprocessing=True):
    """
    Preprocess text with tokenization, stop-word removal, and normalization.
    
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
```

### Frontend Changes (`templates/index.html`)

- Added preprocessing checkbox below comment analysis option
- Passes `apply_preprocessing` boolean to backend API
- Displays preprocessing status in results

## Dependencies Added

```
nltk==3.9.2                       # Natural Language Toolkit
rouge-score==0.1.2                # ROUGE metrics (for Phase 3)
```

### NLTK Data Required

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('stopwords')"
```

## Testing the Feature

1. Start the Flask server:
   ```bash
   source venv/bin/activate
   python app.py
   ```

2. Open http://127.0.0.1:5000 in browser

3. Enter a YouTube URL

4. Check the "Apply NLP preprocessing" checkbox

5. Click "Analyze Video"

6. Compare summary quality with/without preprocessing

## Expected Behavior

### Without Preprocessing (Default)
- Full transcript with punctuation, stop words, mixed case
- More natural language for summarization
- Better context preservation

### With Preprocessing
- Reduced transcript size (30-50% shorter)
- No punctuation or stop words
- All lowercase tokens
- May affect summary quality depending on video content

## Example Comparison

### Original Transcript
```
"Hello everyone! Welcome to this video. Today, we're going to talk about machine learning."
```

### After Preprocessing
```
"hello everyone welcome video today going talk machine learning"
```

## Academic Compliance

✅ **Tokenization**: Implemented using NLTK word_tokenize  
✅ **Stop-word Removal**: Using NLTK stopwords corpus (English)  
✅ **Text Normalization**: Lowercase conversion + punctuation removal  
✅ **Optional Feature**: Can be enabled/disabled via UI checkbox  

## Next Steps (Phase 2)

- Add support for multiple Gemini models
- Compare model performance (gemini-2.0-flash, gemini-2.5-flash, gemini-2.5-pro)
- Store results for side-by-side comparison
- Add model selection dropdown in UI

## Notes

- Preprocessing is **optional** by design - users can compare results
- Some videos benefit from preprocessing (long, repetitive content)
- Others perform better without preprocessing (technical content, proper nouns)
- The feature allows academic evaluation of preprocessing impact on summarization quality
