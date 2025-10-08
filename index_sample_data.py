"""
Sample data and utilities for indexing documents into Elasticsearch.
"""
from search_assistant import AISearchAssistant
from config import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Sample documents about various topics
SAMPLE_DOCUMENTS = [
    {
        "id": "doc1",
        "title": "Introduction to Artificial Intelligence",
        "content": """Artificial Intelligence (AI) is the simulation of human intelligence processes by machines, 
        especially computer systems. These processes include learning, reasoning, and self-correction. 
        AI applications include expert systems, natural language processing, speech recognition, and machine vision. 
        Machine learning is a subset of AI that enables systems to learn and improve from experience without being explicitly programmed.""",
        "metadata": {"category": "AI", "author": "Tech Writer"}
    },
    {
        "id": "doc2",
        "title": "Understanding Machine Learning",
        "content": """Machine Learning is a method of data analysis that automates analytical model building. 
        It is a branch of artificial intelligence based on the idea that systems can learn from data, 
        identify patterns and make decisions with minimal human intervention. Types of machine learning include 
        supervised learning, unsupervised learning, and reinforcement learning. Deep learning is a specialized 
        subset of machine learning that uses neural networks.""",
        "metadata": {"category": "ML", "author": "Data Scientist"}
    },
    {
        "id": "doc3",
        "title": "Natural Language Processing Basics",
        "content": """Natural Language Processing (NLP) is a branch of artificial intelligence that helps computers 
        understand, interpret and manipulate human language. NLP draws from many disciplines, including computer science 
        and computational linguistics. Common NLP tasks include sentiment analysis, named entity recognition, 
        machine translation, and question answering. Modern NLP heavily relies on deep learning and transformer models.""",
        "metadata": {"category": "NLP", "author": "AI Researcher"}
    },
    {
        "id": "doc4",
        "title": "Cloud Computing Fundamentals",
        "content": """Cloud computing is the delivery of computing services including servers, storage, databases, 
        networking, software, analytics, and intelligence over the Internet. Major cloud providers include 
        Amazon Web Services (AWS), Microsoft Azure, and Google Cloud Platform (GCP). Cloud computing offers 
        benefits like cost savings, scalability, performance, and reliability. Service models include 
        Infrastructure as a Service (IaaS), Platform as a Service (PaaS), and Software as a Service (SaaS).""",
        "metadata": {"category": "Cloud", "author": "Cloud Architect"}
    },
    {
        "id": "doc5",
        "title": "Elasticsearch and Search Technologies",
        "content": """Elasticsearch is a distributed, RESTful search and analytics engine capable of addressing 
        a growing number of use cases. It provides real-time search, full-text search, and analytics capabilities. 
        Elasticsearch uses inverted indexes for fast text searches and supports vector search for semantic similarity. 
        Hybrid search combines traditional keyword search with semantic search using embeddings, providing 
        more accurate and relevant results.""",
        "metadata": {"category": "Search", "author": "Search Engineer"}
    },
    {
        "id": "doc6",
        "title": "Large Language Models and Transformers",
        "content": """Large Language Models (LLMs) are AI models trained on vast amounts of text data to understand 
        and generate human-like text. Examples include GPT-4, Claude, and Gemini. The transformer architecture, 
        introduced in the paper 'Attention is All You Need', revolutionized NLP. Transformers use self-attention 
        mechanisms to process sequential data in parallel. LLMs can perform various tasks like text generation, 
        summarization, translation, and question answering through prompting.""",
        "metadata": {"category": "AI", "author": "ML Engineer"}
    },
    {
        "id": "doc7",
        "title": "Vector Databases and Embeddings",
        "content": """Vector databases are specialized databases designed to store and query high-dimensional vectors, 
        typically used for similarity search. Embeddings are dense vector representations of data that capture 
        semantic meaning. Popular vector databases include Pinecone, Weaviate, and Elasticsearch with vector support. 
        Applications include semantic search, recommendation systems, and retrieval-augmented generation (RAG). 
        Vector similarity is typically measured using cosine similarity or Euclidean distance.""",
        "metadata": {"category": "Database", "author": "Data Engineer"}
    },
    {
        "id": "doc8",
        "title": "DevOps and CI/CD Practices",
        "content": """DevOps is a set of practices that combines software development and IT operations. 
        It aims to shorten the development lifecycle and provide continuous delivery with high quality. 
        Key practices include continuous integration (CI), continuous delivery (CD), infrastructure as code, 
        monitoring and logging, and collaboration. Popular tools include Jenkins, GitLab CI, GitHub Actions, 
        Docker, and Kubernetes. DevOps culture emphasizes automation, collaboration, and rapid feedback.""",
        "metadata": {"category": "DevOps", "author": "DevOps Engineer"}
    },
    {
        "id": "doc9",
        "title": "Python Programming for Data Science",
        "content": """Python is a versatile programming language widely used in data science, machine learning, 
        and artificial intelligence. Key libraries include NumPy for numerical computing, Pandas for data manipulation, 
        Scikit-learn for machine learning, TensorFlow and PyTorch for deep learning, and Matplotlib for visualization. 
        Python's simplicity and extensive ecosystem make it ideal for rapid prototyping and production deployment. 
        Jupyter notebooks provide an interactive environment for data exploration and analysis.""",
        "metadata": {"category": "Programming", "author": "Software Developer"}
    },
    {
        "id": "doc10",
        "title": "API Design and RESTful Services",
        "content": """REST (Representational State Transfer) is an architectural style for designing networked applications. 
        RESTful APIs use HTTP methods (GET, POST, PUT, DELETE) to perform CRUD operations. Best practices include 
        using meaningful resource names, proper HTTP status codes, versioning, authentication and authorization, 
        and documentation. Modern alternatives include GraphQL and gRPC. API design should focus on simplicity, 
        consistency, and developer experience. Tools like Swagger/OpenAPI help document and test APIs.""",
        "metadata": {"category": "Web Development", "author": "Backend Developer"}
    }
]


def index_sample_data(assistant: AISearchAssistant):
    """Index sample documents into Elasticsearch."""
    logger.info("Starting to index sample documents...")
    
    # Create index
    assistant.setup_index()
    
    # Index documents
    success_count = 0
    for doc in SAMPLE_DOCUMENTS:
        if assistant.index_document(
            doc_id=doc["id"],
            title=doc["title"],
            content=doc["content"],
            metadata=doc["metadata"]
        ):
            success_count += 1
    
    logger.info(f"Successfully indexed {success_count}/{len(SAMPLE_DOCUMENTS)} documents")
    return success_count


def main():
    """Main function to index sample data."""
    print("Indexing sample data into Elasticsearch...")
    
    try:
        # Initialize assistant
        assistant = AISearchAssistant()
        
        # Index sample data
        count = index_sample_data(assistant)
        
        print(f"\n✓ Successfully indexed {count} sample documents!")
        print("\nYou can now use the search assistant with:")
        print("  python cli.py")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nMake sure:")
        print("  1. Elasticsearch is running")
        print("  2. Configuration is set up correctly")
        print("  3. All dependencies are installed")


if __name__ == "__main__":
    main()
