"""
Google Cloud Vertex AI and Gemini integration for AI reasoning.
"""
import logging
from typing import List, Dict, Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GeminiClient:
    """Client for interacting with Google's Gemini AI."""
    
    def __init__(self, api_key: str = "", project_id: str = ""):
        """Initialize Gemini client."""
        self.api_key = api_key
        self.project_id = project_id
        self.model = None
        
        # Try to initialize Gemini
        if api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-pro')
                logger.info("Successfully initialized Gemini client")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini: {e}")
        
        # Fallback to Vertex AI if Gemini fails
        if not self.model and project_id:
            try:
                from google.cloud import aiplatform
                aiplatform.init(project=project_id)
                logger.info("Successfully initialized Vertex AI client")
            except Exception as e:
                logger.error(f"Failed to initialize Vertex AI: {e}")
    
    def generate_response(self, prompt: str, context: Optional[str] = None,
                         temperature: float = 0.7) -> str:
        """Generate a response using Gemini."""
        if not self.model:
            logger.warning("Gemini model not initialized, using fallback response")
            return self._fallback_response(prompt, context)
        
        try:
            # Build the full prompt with context
            full_prompt = self._build_prompt(prompt, context)
            
            # Generate response
            response = self.model.generate_content(
                full_prompt,
                generation_config={
                    'temperature': temperature,
                    'max_output_tokens': 1024,
                }
            )
            
            return response.text
        except Exception as e:
            logger.error(f"Failed to generate response: {e}")
            return self._fallback_response(prompt, context)
    
    def _build_prompt(self, query: str, context: Optional[str] = None) -> str:
        """Build a prompt with context for the AI model."""
        if context:
            return f"""You are an intelligent search assistant. Use the following search results to answer the user's question.

Search Results:
{context}

User Question: {query}

Provide a comprehensive, accurate, and helpful response based on the search results. If the search results don't contain enough information to answer the question, acknowledge that and provide what information is available."""
        else:
            return f"""You are an intelligent search assistant. The user asked: {query}

Provide a helpful response based on your knowledge."""
    
    def _fallback_response(self, query: str, context: Optional[str] = None) -> str:
        """Provide a fallback response when AI model is unavailable."""
        if context:
            return f"Based on the search results, here's what I found:\n\n{context}\n\nPlease review these results for information about: {query}"
        else:
            return f"I'm currently running in offline mode. I would need access to search results to answer: {query}"
    
    def summarize_results(self, results: List[Dict[str, Any]]) -> str:
        """Summarize search results into a context string."""
        if not results:
            return "No search results found."
        
        context_parts = []
        for i, result in enumerate(results, 1):
            title = result.get('title', 'Untitled')
            content = result.get('content', '')
            # Truncate long content
            content_preview = content[:300] + "..." if len(content) > 300 else content
            context_parts.append(f"{i}. {title}\n{content_preview}")
        
        return "\n\n".join(context_parts)
    
    def chat(self, message: str, conversation_history: List[Dict[str, str]],
             search_context: Optional[str] = None) -> str:
        """Have a conversation with context awareness."""
        # Build conversation context
        conversation_text = ""
        for msg in conversation_history[-5:]:  # Last 5 messages
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            conversation_text += f"{role.upper()}: {content}\n"
        
        # Build full prompt with conversation history and search context
        full_prompt = ""
        if search_context:
            full_prompt += f"Search Results:\n{search_context}\n\n"
        
        if conversation_text:
            full_prompt += f"Conversation History:\n{conversation_text}\n"
        
        full_prompt += f"USER: {message}\n\nASSISTANT:"
        
        return self.generate_response(message, full_prompt)
