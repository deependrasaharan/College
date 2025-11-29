"""
Configuration module for YouTube NLP Analyzer.
Handles environment variables and API settings.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration settings for the application."""
    
    # OpenAI API settings
    OPENAI_API_KEY: Optional[str] = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL: str = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    
    # Default temperature settings
    DEFAULT_TEMPERATURE: float = float(os.getenv('DEFAULT_TEMPERATURE', '0.7'))
    MIN_TEMPERATURE: float = 0.0
    MAX_TEMPERATURE: float = 2.0
    
    # Summary settings
    DEFAULT_MAX_TOKENS: int = int(os.getenv('DEFAULT_MAX_TOKENS', '500'))
    MAX_INPUT_CHARS: int = 12000  # Roughly 3000 tokens for GPT-3.5
    
    # Transcript settings
    DEFAULT_LANGUAGE: str = os.getenv('DEFAULT_LANGUAGE', 'en')
    
    @classmethod
    def validate(cls) -> bool:
        """
        Validate configuration settings.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        if not cls.OPENAI_API_KEY:
            print("Warning: OPENAI_API_KEY not set in environment variables.")
            print("You can still extract transcripts, but summarization won't work.")
            return False
        
        if not (cls.MIN_TEMPERATURE <= cls.DEFAULT_TEMPERATURE <= cls.MAX_TEMPERATURE):
            print(f"Error: DEFAULT_TEMPERATURE must be between {cls.MIN_TEMPERATURE} and {cls.MAX_TEMPERATURE}")
            return False
        
        return True
    
    @classmethod
    def display(cls):
        """Display current configuration (without sensitive data)."""
        print("Current Configuration:")
        print(f"  Model: {cls.OPENAI_MODEL}")
        print(f"  Default Temperature: {cls.DEFAULT_TEMPERATURE}")
        print(f"  Default Max Tokens: {cls.DEFAULT_MAX_TOKENS}")
        print(f"  Default Language: {cls.DEFAULT_LANGUAGE}")
        print(f"  API Key Set: {'Yes' if cls.OPENAI_API_KEY else 'No'}")


if __name__ == "__main__":
    Config.validate()
    Config.display()
