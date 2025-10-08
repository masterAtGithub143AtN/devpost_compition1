"""
Main AI Search Assistant combining Elasticsearch hybrid search with Gemini AI.
"""
import logging
from typing import List, Dict, Any, Optional
from elasticsearch_client import ElasticSearchClient
from gemini_client import GeminiClient
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AISearchAssistant:
    """Intelligent, interactive, and context-aware AI search assistant."""
    
    def __init__(self, config: Config = None):
        """Initialize the AI Search Assistant."""
        self.config = config or Config()
        
        # Initialize Elasticsearch client
        self.search_client = ElasticSearchClient(
            host=self.config.ELASTICSEARCH_HOST,
            port=self.config.ELASTICSEARCH_PORT,
            user=self.config.ELASTICSEARCH_USER,
            password=self.config.ELASTICSEARCH_PASSWORD,
            index_name=self.config.ELASTICSEARCH_INDEX
        )
        
        # Initialize Gemini client
        self.ai_client = GeminiClient(
            api_key=self.config.GEMINI_API_KEY,
            project_id=self.config.GOOGLE_CLOUD_PROJECT
        )
        
        # Conversation history
        self.conversation_history: List[Dict[str, str]] = []
        
        logger.info("AI Search Assistant initialized")
    
    def setup_index(self):
        """Set up the Elasticsearch index."""
        return self.search_client.create_index()
    
    def index_document(self, doc_id: str, title: str, content: str, 
                      metadata: Optional[Dict] = None):
        """Index a document into the search engine."""
        return self.search_client.index_document(doc_id, title, content, metadata)
    
    def search(self, query: str, max_results: Optional[int] = None) -> List[Dict[str, Any]]:
        """Perform hybrid search."""
        max_results = max_results or self.config.MAX_SEARCH_RESULTS
        
        results = self.search_client.hybrid_search(
            query=query,
            semantic_weight=self.config.HYBRID_SEARCH_WEIGHT_SEMANTIC,
            keyword_weight=self.config.HYBRID_SEARCH_WEIGHT_KEYWORD,
            size=max_results
        )
        
        return results
    
    def ask(self, question: str, use_search: bool = True) -> Dict[str, Any]:
        """
        Ask a question and get an AI-powered response with search context.
        
        Args:
            question: The user's question
            use_search: Whether to perform a search for context
        
        Returns:
            Dictionary containing the response and search results
        """
        logger.info(f"Processing question: {question}")
        
        # Perform hybrid search if enabled
        search_results = []
        if use_search:
            search_results = self.search(question)
        
        # Generate context from search results
        search_context = self.ai_client.summarize_results(search_results) if search_results else None
        
        # Generate AI response
        response = self.ai_client.generate_response(question, search_context)
        
        # Update conversation history
        self.conversation_history.append({
            "role": "user",
            "content": question
        })
        self.conversation_history.append({
            "role": "assistant",
            "content": response
        })
        
        # Maintain conversation history length
        if len(self.conversation_history) > self.config.CONVERSATION_CONTEXT_LENGTH * 2:
            self.conversation_history = self.conversation_history[-self.config.CONVERSATION_CONTEXT_LENGTH * 2:]
        
        return {
            "question": question,
            "response": response,
            "search_results": search_results,
            "context_used": search_context is not None
        }
    
    def chat(self, message: str) -> str:
        """
        Have a conversation with context awareness.
        
        Args:
            message: The user's message
        
        Returns:
            AI assistant's response
        """
        logger.info(f"Chat message: {message}")
        
        # Perform search for relevant context
        search_results = self.search(message, max_results=3)
        search_context = self.ai_client.summarize_results(search_results) if search_results else None
        
        # Generate response with conversation history
        response = self.ai_client.chat(message, self.conversation_history, search_context)
        
        # Update conversation history
        self.conversation_history.append({
            "role": "user",
            "content": message
        })
        self.conversation_history.append({
            "role": "assistant",
            "content": response
        })
        
        # Maintain conversation history length
        if len(self.conversation_history) > self.config.CONVERSATION_CONTEXT_LENGTH * 2:
            self.conversation_history = self.conversation_history[-self.config.CONVERSATION_CONTEXT_LENGTH * 2:]
        
        return response
    
    def clear_conversation(self):
        """Clear the conversation history."""
        self.conversation_history = []
        logger.info("Conversation history cleared")
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get the current conversation history."""
        return self.conversation_history
