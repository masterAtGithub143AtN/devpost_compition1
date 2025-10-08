"""
Elasticsearch client with hybrid search capabilities.
"""
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ElasticSearchClient:
    """Client for interacting with Elasticsearch with hybrid search support."""
    
    def __init__(self, host: str = "localhost", port: int = 9200, 
                 user: str = "elastic", password: str = "", 
                 index_name: str = "search_assistant"):
        """Initialize Elasticsearch client."""
        self.index_name = index_name
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize Elasticsearch client
        try:
            if password:
                self.client = Elasticsearch(
                    [f"http://{host}:{port}"],
                    basic_auth=(user, password)
                )
            else:
                self.client = Elasticsearch([f"http://{host}:{port}"])
            
            # Check connection
            if self.client.ping():
                logger.info("Successfully connected to Elasticsearch")
            else:
                logger.warning("Elasticsearch connection check failed")
        except Exception as e:
            logger.error(f"Failed to connect to Elasticsearch: {e}")
            self.client = None
    
    def create_index(self):
        """Create index with mappings for hybrid search."""
        if not self.client:
            logger.error("Elasticsearch client not initialized")
            return False
        
        mapping = {
            "mappings": {
                "properties": {
                    "title": {"type": "text"},
                    "content": {"type": "text"},
                    "embedding": {
                        "type": "dense_vector",
                        "dims": 384,
                        "index": True,
                        "similarity": "cosine"
                    },
                    "metadata": {"type": "object"},
                    "timestamp": {"type": "date"}
                }
            }
        }
        
        try:
            if self.client.indices.exists(index=self.index_name):
                logger.info(f"Index {self.index_name} already exists")
                return True
            
            self.client.indices.create(index=self.index_name, body=mapping)
            logger.info(f"Created index: {self.index_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to create index: {e}")
            return False
    
    def index_document(self, doc_id: str, title: str, content: str, 
                      metadata: Optional[Dict] = None):
        """Index a document with embeddings."""
        if not self.client:
            logger.error("Elasticsearch client not initialized")
            return False
        
        try:
            # Generate embedding
            embedding = self.embedding_model.encode(content).tolist()
            
            document = {
                "title": title,
                "content": content,
                "embedding": embedding,
                "metadata": metadata or {},
            }
            
            self.client.index(index=self.index_name, id=doc_id, document=document)
            logger.info(f"Indexed document: {doc_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to index document: {e}")
            return False
    
    def hybrid_search(self, query: str, semantic_weight: float = 0.6, 
                     keyword_weight: float = 0.4, size: int = 5) -> List[Dict[str, Any]]:
        """Perform hybrid search combining semantic and keyword search."""
        if not self.client:
            logger.error("Elasticsearch client not initialized")
            return []
        
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode(query).tolist()
            
            # Semantic search query
            semantic_query = {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                        "params": {"query_vector": query_embedding}
                    }
                }
            }
            
            # Keyword search query
            keyword_query = {
                "multi_match": {
                    "query": query,
                    "fields": ["title^2", "content"],
                    "type": "best_fields"
                }
            }
            
            # Combined query with weighted scores
            search_query = {
                "query": {
                    "bool": {
                        "should": [
                            {"constant_score": {
                                "filter": semantic_query,
                                "boost": semantic_weight
                            }},
                            {"constant_score": {
                                "filter": keyword_query,
                                "boost": keyword_weight
                            }}
                        ]
                    }
                },
                "size": size
            }
            
            response = self.client.search(index=self.index_name, body=search_query)
            
            results = []
            for hit in response['hits']['hits']:
                results.append({
                    "id": hit["_id"],
                    "score": hit["_score"],
                    "title": hit["_source"].get("title", ""),
                    "content": hit["_source"].get("content", ""),
                    "metadata": hit["_source"].get("metadata", {})
                })
            
            logger.info(f"Found {len(results)} results for query: {query}")
            return results
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []
    
    def delete_index(self):
        """Delete the index."""
        if not self.client:
            logger.error("Elasticsearch client not initialized")
            return False
        
        try:
            if self.client.indices.exists(index=self.index_name):
                self.client.indices.delete(index=self.index_name)
                logger.info(f"Deleted index: {self.index_name}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to delete index: {e}")
            return False
