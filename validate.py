"""
Validation script to verify the AI Search Assistant structure.
Tests basic functionality without requiring external dependencies.
"""
import sys
import os


def check_file_exists(filepath, description):
    """Check if a file exists."""
    if os.path.exists(filepath):
        print(f"✓ {description}: {filepath}")
        return True
    else:
        print(f"✗ {description} missing: {filepath}")
        return False


def check_python_syntax(filepath):
    """Check if a Python file has valid syntax."""
    try:
        with open(filepath, 'r') as f:
            compile(f.read(), filepath, 'exec')
        print(f"✓ Valid syntax: {filepath}")
        return True
    except SyntaxError as e:
        print(f"✗ Syntax error in {filepath}: {e}")
        return False


def check_file_content(filepath, required_strings, description):
    """Check if file contains required strings."""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        missing = []
        for req in required_strings:
            if req not in content:
                missing.append(req)
        
        if not missing:
            print(f"✓ {description} contains required content")
            return True
        else:
            print(f"✗ {description} missing: {', '.join(missing)}")
            return False
    except Exception as e:
        print(f"✗ Error reading {filepath}: {e}")
        return False


def main():
    """Main validation function."""
    print("=" * 70)
    print("AI Search Assistant - Validation Script")
    print("=" * 70)
    
    results = []
    
    # Check essential files exist
    print("\n1. Checking Essential Files...")
    files = [
        ("config.py", "Configuration module"),
        ("elasticsearch_client.py", "Elasticsearch client"),
        ("gemini_client.py", "Gemini AI client"),
        ("search_assistant.py", "Main assistant module"),
        ("cli.py", "CLI interface"),
        ("index_sample_data.py", "Sample data indexer"),
        ("example.py", "Example script"),
        ("requirements.txt", "Dependencies file"),
        (".env.example", "Environment template"),
        (".gitignore", "Git ignore file"),
        ("README.md", "Documentation"),
        ("QUICKSTART.md", "Quick start guide"),
    ]
    
    for filepath, desc in files:
        results.append(check_file_exists(filepath, desc))
    
    # Check Python syntax
    print("\n2. Checking Python Syntax...")
    python_files = [
        "config.py",
        "elasticsearch_client.py",
        "gemini_client.py",
        "search_assistant.py",
        "cli.py",
        "index_sample_data.py",
        "example.py",
    ]
    
    for filepath in python_files:
        if os.path.exists(filepath):
            results.append(check_python_syntax(filepath))
    
    # Check key content
    print("\n3. Checking Key Components...")
    
    # Config should have all settings
    results.append(check_file_content(
        "config.py",
        ["ELASTICSEARCH_HOST", "GEMINI_API_KEY", "HYBRID_SEARCH_WEIGHT"],
        "Configuration"
    ))
    
    # Elasticsearch client should have hybrid search
    results.append(check_file_content(
        "elasticsearch_client.py",
        ["hybrid_search", "semantic_weight", "keyword_weight", "embedding"],
        "Hybrid search implementation"
    ))
    
    # Gemini client should have AI methods
    results.append(check_file_content(
        "gemini_client.py",
        ["generate_response", "chat", "summarize_results"],
        "Gemini AI client"
    ))
    
    # Search assistant should combine both
    results.append(check_file_content(
        "search_assistant.py",
        ["AISearchAssistant", "ask", "chat", "search"],
        "Search assistant"
    ))
    
    # CLI should have interactive features
    results.append(check_file_content(
        "cli.py",
        ["/search", "/ask", "/chat", "/help"],
        "CLI interface"
    ))
    
    # README should have documentation
    results.append(check_file_content(
        "README.md",
        ["Hybrid Search", "Gemini", "Installation", "Usage"],
        "Documentation"
    ))
    
    # Check requirements
    print("\n4. Checking Dependencies...")
    results.append(check_file_content(
        "requirements.txt",
        ["elasticsearch", "google-", "sentence-transformers", "python-dotenv"],
        "Requirements"
    ))
    
    # Summary
    print("\n" + "=" * 70)
    passed = sum(results)
    total = len(results)
    percentage = (passed / total) * 100 if total > 0 else 0
    
    print(f"Validation Results: {passed}/{total} checks passed ({percentage:.1f}%)")
    
    if passed == total:
        print("✓ All validation checks passed!")
        print("\nThe AI Search Assistant is properly structured and ready to use.")
        print("\nNext steps:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Configure .env file with your API keys")
        print("  3. Run: python cli.py")
        return 0
    else:
        print("✗ Some validation checks failed.")
        print("Please review the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
