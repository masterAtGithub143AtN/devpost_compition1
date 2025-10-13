"""
Configuration management for the AI Search Assistant.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the search assistant."""
    
    # Elasticsearch settings
    ELASTICSEARCH_HOST = os.getenv("ELASTICSEARCH_HOST", "localhost")
    ELASTICSEARCH_PORT = int(os.getenv("ELASTICSEARCH_PORT", "9200"))
    ELASTICSEARCH_USER = os.getenv("ELASTICSEARCH_USER", "elastic")
    ELASTICSEARCH_PASSWORD = os.getenv("ELASTICSEARCH_PASSWORD", "")
    ELASTICSEARCH_INDEX = os.getenv("ELASTICSEARCH_INDEX", "search_assistant")
    
    # Google Cloud settings
    GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "")
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    
    # Search settings
    HYBRID_SEARCH_WEIGHT_SEMANTIC = float(os.getenv("HYBRID_SEARCH_WEIGHT_SEMANTIC", "0.6"))
    HYBRID_SEARCH_WEIGHT_KEYWORD = float(os.getenv("HYBRID_SEARCH_WEIGHT_KEYWORD", "0.4"))
    MAX_SEARCH_RESULTS = int(os.getenv("MAX_SEARCH_RESULTS", "5"))
    CONVERSATION_CONTEXT_LENGTH = int(os.getenv("CONVERSATION_CONTEXT_LENGTH", "5"))
    
    @classmethod
    def validate(cls):
        """Validate required configuration."""
        required = []
        if not cls.GEMINI_API_KEY and not cls.GOOGLE_CLOUD_PROJECT:
            required.append("GEMINI_API_KEY or GOOGLE_CLOUD_PROJECT")
        
        if required:
            raise ValueError(f"Missing required configuration: {', '.join(required)}")
        
        return True
