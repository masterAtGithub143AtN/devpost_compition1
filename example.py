"""
Simple example demonstrating the AI Search Assistant usage.
"""
from search_assistant import AISearchAssistant
from config import Config

def main():
    """Example usage of the AI Search Assistant."""
    
    print("=== AI Search Assistant Example ===\n")
    
    # Initialize the assistant
    print("1. Initializing AI Search Assistant...")
    assistant = AISearchAssistant()
    
    # Example 1: Search
    print("\n2. Performing hybrid search...")
    query = "machine learning"
    results = assistant.search(query, max_results=3)
    
    print(f"\nSearch results for '{query}':")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['title']}")
        print(f"   Score: {result['score']:.4f}")
        print(f"   Content: {result['content'][:150]}...")
    
    # Example 2: Ask a question
    print("\n\n3. Asking a question with AI reasoning...")
    question = "What is the relationship between AI and machine learning?"
    response = assistant.ask(question)
    
    print(f"\nQuestion: {question}")
    print(f"\nAI Response:\n{response['response']}")
    
    # Example 3: Chat conversation
    print("\n\n4. Having a conversation...")
    messages = [
        "Tell me about natural language processing",
        "How is it used in practice?",
        "What are some popular NLP models?"
    ]
    
    for msg in messages:
        print(f"\nYou: {msg}")
        response = assistant.chat(msg)
        print(f"Assistant: {response[:200]}...")
    
    # Example 4: Show conversation history
    print("\n\n5. Conversation history:")
    history = assistant.get_conversation_history()
    print(f"Total messages in history: {len(history)}")
    
    print("\n=== Example Complete ===")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nError: {e}")
        print("\nMake sure:")
        print("  1. You have configured your .env file")
        print("  2. Elasticsearch is running (if using)")
        print("  3. You have indexed some sample data: python index_sample_data.py")
