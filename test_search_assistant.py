"""
Basic tests for the AI Search Assistant components.
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
from config import Config
from elasticsearch_client import ElasticSearchClient
from gemini_client import GeminiClient
from search_assistant import AISearchAssistant


class TestConfig(unittest.TestCase):
    """Test configuration management."""
    
    def test_config_defaults(self):
        """Test default configuration values."""
        self.assertEqual(Config.ELASTICSEARCH_HOST, "localhost")
        self.assertEqual(Config.ELASTICSEARCH_PORT, 9200)
        self.assertEqual(Config.HYBRID_SEARCH_WEIGHT_SEMANTIC, 0.6)
        self.assertEqual(Config.HYBRID_SEARCH_WEIGHT_KEYWORD, 0.4)
    
    def test_config_validate(self):
        """Test configuration validation."""
        # Should pass if at least one AI method is configured
        with patch.object(Config, 'GEMINI_API_KEY', 'test_key'):
            self.assertTrue(Config.validate())


class TestElasticSearchClient(unittest.TestCase):
    """Test Elasticsearch client."""
    
    @patch('elasticsearch_client.Elasticsearch')
    @patch('elasticsearch_client.SentenceTransformer')
    def test_initialization(self, mock_transformer, mock_es):
        """Test client initialization."""
        mock_es_instance = Mock()
        mock_es.return_value = mock_es_instance
        mock_es_instance.ping.return_value = True
        
        client = ElasticSearchClient(host="localhost", port=9200)
        
        self.assertIsNotNone(client)
        self.assertEqual(client.index_name, "search_assistant")
    
    @patch('elasticsearch_client.Elasticsearch')
    @patch('elasticsearch_client.SentenceTransformer')
    def test_create_index(self, mock_transformer, mock_es):
        """Test index creation."""
        mock_es_instance = Mock()
        mock_es.return_value = mock_es_instance
        mock_es_instance.ping.return_value = True
        mock_es_instance.indices.exists.return_value = False
        
        client = ElasticSearchClient()
        result = client.create_index()
        
        self.assertTrue(result)
        mock_es_instance.indices.create.assert_called_once()


class TestGeminiClient(unittest.TestCase):
    """Test Gemini AI client."""
    
    def test_fallback_response(self):
        """Test fallback response when model is unavailable."""
        client = GeminiClient(api_key="", project_id="")
        response = client._fallback_response("test query", "test context")
        
        self.assertIn("test query", response)
        self.assertIn("test context", response)
    
    def test_summarize_results(self):
        """Test results summarization."""
        client = GeminiClient(api_key="", project_id="")
        results = [
            {"title": "Title 1", "content": "Content 1"},
            {"title": "Title 2", "content": "Content 2"}
        ]
        
        summary = client.summarize_results(results)
        
        self.assertIn("Title 1", summary)
        self.assertIn("Title 2", summary)
        self.assertIn("Content 1", summary)
        self.assertIn("Content 2", summary)
    
    def test_empty_results(self):
        """Test summarization with empty results."""
        client = GeminiClient(api_key="", project_id="")
        summary = client.summarize_results([])
        
        self.assertEqual(summary, "No search results found.")


class TestAISearchAssistant(unittest.TestCase):
    """Test main search assistant."""
    
    @patch('search_assistant.GeminiClient')
    @patch('search_assistant.ElasticSearchClient')
    def test_initialization(self, mock_es, mock_gemini):
        """Test assistant initialization."""
        assistant = AISearchAssistant()
        
        self.assertIsNotNone(assistant)
        self.assertEqual(len(assistant.conversation_history), 0)
    
    @patch('search_assistant.GeminiClient')
    @patch('search_assistant.ElasticSearchClient')
    def test_clear_conversation(self, mock_es, mock_gemini):
        """Test conversation clearing."""
        assistant = AISearchAssistant()
        assistant.conversation_history = [{"role": "user", "content": "test"}]
        
        assistant.clear_conversation()
        
        self.assertEqual(len(assistant.conversation_history), 0)
    
    @patch('search_assistant.GeminiClient')
    @patch('search_assistant.ElasticSearchClient')
    def test_conversation_history_limit(self, mock_es, mock_gemini):
        """Test that conversation history is limited."""
        mock_gemini_instance = Mock()
        mock_gemini.return_value = mock_gemini_instance
        mock_gemini_instance.chat.return_value = "response"
        
        mock_es_instance = Mock()
        mock_es.return_value = mock_es_instance
        mock_es_instance.hybrid_search.return_value = []
        
        assistant = AISearchAssistant()
        
        # Add more messages than the limit
        for i in range(20):
            assistant.conversation_history.append({
                "role": "user", 
                "content": f"message {i}"
            })
        
        assistant.chat("new message")
        
        # Should be limited to CONVERSATION_CONTEXT_LENGTH * 2 + 2 (for the new pair)
        max_expected = Config.CONVERSATION_CONTEXT_LENGTH * 2 + 2
        self.assertLessEqual(len(assistant.conversation_history), max_expected)


class TestIntegration(unittest.TestCase):
    """Integration tests."""
    
    @patch('search_assistant.GeminiClient')
    @patch('search_assistant.ElasticSearchClient')
    def test_ask_without_search(self, mock_es, mock_gemini):
        """Test asking without search enabled."""
        mock_gemini_instance = Mock()
        mock_gemini.return_value = mock_gemini_instance
        mock_gemini_instance.generate_response.return_value = "AI response"
        mock_gemini_instance.summarize_results.return_value = None
        
        assistant = AISearchAssistant()
        result = assistant.ask("test question", use_search=False)
        
        self.assertEqual(result["question"], "test question")
        self.assertEqual(result["response"], "AI response")
        self.assertFalse(result["context_used"])


if __name__ == "__main__":
    unittest.main()
