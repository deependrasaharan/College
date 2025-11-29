"""
Sentiment Analysis Evaluation Script
Compares TextBlob sentiment analysis with labeled YouTube comments dataset
"""

import pandas as pd
from textblob import TextBlob
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix, classification_report
import numpy as np

def analyze_sentiment_textblob(text):
    """
    Analyze sentiment using TextBlob (same logic as app.py)
    Returns: 'Positive', 'Negative', or 'Neutral'
    """
    try:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        if polarity > 0.1:
            return 'Positive'
        elif polarity < -0.1:
            return 'Negative'
        else:
            return 'Neutral'
    except:
        return 'Neutral'  # Default for errors

def evaluate_sentiment_model(csv_path='youtube_comments_cleaned.csv', sample_size=1000):
    """
    Evaluate TextBlob sentiment analysis against labeled dataset
    """
    print("="*80)
    print("SENTIMENT ANALYSIS EVALUATION")
    print("="*80)
    
    # Load dataset
    print(f"\n📁 Loading dataset: {csv_path}")
    df = pd.read_csv(csv_path)
    
    print(f"   Total comments in dataset: {len(df):,}")
    
    # Filter English comments (remove non-English to improve evaluation accuracy)
    df = df[df['CommentText'].str.strip().str.len() > 0]  # Remove empty
    
    # Sample data if needed
    if len(df) > sample_size:
        print(f"   Sampling {sample_size:,} comments for evaluation...")
        df = df.sample(n=sample_size, random_state=42)
    
    print(f"\n📊 Sentiment Distribution in Dataset:")
    print(df['Sentiment'].value_counts())
    print(f"\n   Using {len(df):,} comments for evaluation")
    
    # Apply TextBlob sentiment analysis
    print("\n🔍 Analyzing sentiments with TextBlob...")
    df['Predicted_Sentiment'] = df['CommentText'].apply(analyze_sentiment_textblob)
    
    # Prepare data for evaluation
    y_true = df['Sentiment']
    y_pred = df['Predicted_Sentiment']
    
    # Calculate metrics
    print("\n" + "="*80)
    print("EVALUATION METRICS")
    print("="*80)
    
    # Overall Accuracy
    accuracy = accuracy_score(y_true, y_pred)
    print(f"\n✅ Overall Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    
    # Precision, Recall, F1-Score per class
    precision, recall, f1, support = precision_recall_fscore_support(
        y_true, y_pred, labels=['Positive', 'Negative', 'Neutral'], zero_division=0
    )
    
    print(f"\n📈 Per-Class Metrics:")
    print(f"\n{'Class':<15} {'Precision':<12} {'Recall':<12} {'F1-Score':<12} {'Support'}")
    print("-" * 65)
    
    for i, label in enumerate(['Positive', 'Negative', 'Neutral']):
        print(f"{label:<15} {precision[i]:<12.4f} {recall[i]:<12.4f} {f1[i]:<12.4f} {support[i]}")
    
    # Macro and Weighted Averages
    precision_macro, recall_macro, f1_macro, _ = precision_recall_fscore_support(
        y_true, y_pred, average='macro', zero_division=0
    )
    precision_weighted, recall_weighted, f1_weighted, _ = precision_recall_fscore_support(
        y_true, y_pred, average='weighted', zero_division=0
    )
    
    print("-" * 65)
    print(f"{'Macro Avg':<15} {precision_macro:<12.4f} {recall_macro:<12.4f} {f1_macro:<12.4f}")
    print(f"{'Weighted Avg':<15} {precision_weighted:<12.4f} {recall_weighted:<12.4f} {f1_weighted:<12.4f}")
    
    # Confusion Matrix
    print(f"\n📊 Confusion Matrix:")
    cm = confusion_matrix(y_true, y_pred, labels=['Positive', 'Negative', 'Neutral'])
    print(f"\n{'':>15} {'Predicted'}")
    print(f"{'':>15} {'Positive':<12} {'Negative':<12} {'Neutral':<12}")
    print("-" * 55)
    for i, true_label in enumerate(['Positive', 'Negative', 'Neutral']):
        print(f"{'Actual':<8} {true_label:<6} {cm[i][0]:<12} {cm[i][1]:<12} {cm[i][2]:<12}")
    
    # Detailed Classification Report
    print(f"\n📋 Detailed Classification Report:")
    print(classification_report(y_true, y_pred, labels=['Positive', 'Negative', 'Neutral'], zero_division=0))
    
    # Sample Predictions
    print(f"\n📝 Sample Predictions (First 10):")
    print("-" * 80)
    for idx in range(min(10, len(df))):
        row = df.iloc[idx]
        match = "✅" if row['Sentiment'] == row['Predicted_Sentiment'] else "❌"
        print(f"\n{match} Comment: {row['CommentText'][:70]}...")
        print(f"   Labeled: {row['Sentiment']:<10} | Predicted: {row['Predicted_Sentiment']:<10}")
    
    # Summary Statistics
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total Comments Evaluated: {len(df):,}")
    print(f"Correctly Classified: {int(accuracy * len(df)):,} ({accuracy*100:.2f}%)")
    print(f"Misclassified: {int((1-accuracy) * len(df)):,} ({(1-accuracy)*100:.2f}%)")
    print(f"\nBest Performing Class (F1): {['Positive', 'Negative', 'Neutral'][np.argmax(f1)]}")
    print(f"Worst Performing Class (F1): {['Positive', 'Negative', 'Neutral'][np.argmin(f1)]}")
    
    # Save detailed results
    results_df = df[['CommentText', 'Sentiment', 'Predicted_Sentiment']].copy()
    results_df['Correct'] = results_df['Sentiment'] == results_df['Predicted_Sentiment']
    results_df.to_csv('sentiment_evaluation_results.csv', index=False)
    print(f"\n💾 Detailed results saved to: sentiment_evaluation_results.csv")
    
    return {
        'accuracy': accuracy,
        'precision_macro': precision_macro,
        'recall_macro': recall_macro,
        'f1_macro': f1_macro,
        'f1_positive': f1[0],
        'f1_negative': f1[1],
        'f1_neutral': f1[2],
        'confusion_matrix': cm
    }

if __name__ == "__main__":
    # Run evaluation
    metrics = evaluate_sentiment_model(sample_size=1000)
    
    print("\n" + "="*80)
    print("✨ Evaluation Complete!")
    print("="*80)
