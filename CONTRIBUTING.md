# Contributing to AI Search Assistant

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project follows a code of conduct to foster an open and welcoming environment:

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect differing viewpoints and experiences
- Accept responsibility and apologize for mistakes

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the behavior
- **Expected behavior**
- **Actual behavior**
- **Environment details** (OS, Python version, etc.)
- **Error messages** or logs
- **Screenshots** if applicable

**Bug Report Template:**

```markdown
## Bug Description
A clear description of the bug.

## Steps to Reproduce
1. Go to '...'
2. Run '...'
3. See error

## Expected Behavior
What you expected to happen.

## Actual Behavior
What actually happened.

## Environment
- OS: [e.g., Ubuntu 22.04]
- Python: [e.g., 3.11]
- Elasticsearch: [e.g., 8.11.0]

## Additional Context
Any other relevant information.
```

### Suggesting Enhancements

Enhancement suggestions are welcome! Please provide:

- **Clear title and description**
- **Use case** - why is this enhancement useful?
- **Proposed solution** - how should it work?
- **Alternatives considered**
- **Additional context**

### Contributing Code

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes**
4. **Test your changes**
5. **Commit with clear messages** (`git commit -m 'Add amazing feature'`)
6. **Push to your fork** (`git push origin feature/amazing-feature`)
7. **Open a Pull Request**

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repo on GitHub, then:
git clone https://github.com/YOUR_USERNAME/devpost_compition1.git
cd devpost_compition1
```

### 2. Set Up Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install flake8 black pytest pytest-cov
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your API keys
```

### 4. Verify Setup

```bash
python validate.py
```

## Coding Standards

### Python Style Guide

Follow [PEP 8](https://pep8.org/) with these specifics:

- **Line Length**: Maximum 100 characters
- **Indentation**: 4 spaces
- **Naming**:
  - `snake_case` for functions and variables
  - `PascalCase` for classes
  - `UPPER_CASE` for constants
- **Docstrings**: Use Google-style docstrings

Example:

```python
class SearchAssistant:
    """Main search assistant class.
    
    This class orchestrates hybrid search and AI reasoning.
    
    Attributes:
        config: Configuration object
        search_client: Elasticsearch client
    """
    
    def search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Perform hybrid search.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
        
        Returns:
            List of search results with scores
        
        Raises:
            ValueError: If query is empty
        """
        if not query:
            raise ValueError("Query cannot be empty")
        
        # Implementation...
```

### Code Formatting

```bash
# Format code with Black
black .

# Check style with flake8
flake8 . --max-line-length=100
```

### Type Hints

Use type hints for function signatures:

```python
from typing import List, Dict, Optional

def process_results(results: List[Dict[str, Any]], 
                   max_count: Optional[int] = None) -> List[Dict[str, Any]]:
    """Process and filter results."""
    # Implementation...
```

## Testing

### Writing Tests

- Place tests in `test_*.py` files
- Use descriptive test names: `test_search_returns_results`
- Mock external dependencies (Elasticsearch, Gemini API)
- Test edge cases and error conditions

Example:

```python
import unittest
from unittest.mock import Mock, patch

class TestSearchAssistant(unittest.TestCase):
    """Test cases for SearchAssistant class."""
    
    @patch('search_assistant.ElasticSearchClient')
    def test_search_with_results(self, mock_es):
        """Test search returns expected results."""
        # Setup
        mock_es.return_value.hybrid_search.return_value = [
            {"title": "Test", "score": 1.0}
        ]
        
        # Execute
        assistant = SearchAssistant()
        results = assistant.search("test query")
        
        # Assert
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Test")
```

### Running Tests

```bash
# Run all tests
python -m unittest discover

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
python -m unittest test_search_assistant.py
```

## Pull Request Process

### Before Submitting

1. **Update documentation** if adding features
2. **Add tests** for new functionality
3. **Run validation**: `python validate.py`
4. **Check code style**: `flake8 .`
5. **Test locally** with your changes
6. **Update CHANGELOG** if applicable

### PR Guidelines

- **Title**: Clear, descriptive summary
- **Description**: What, why, and how
- **Link issues**: Reference related issues
- **Screenshots**: Include for UI changes
- **Tests**: Show tests pass
- **Documentation**: Note any doc updates

**PR Template:**

```markdown
## Description
Brief description of changes.

## Motivation
Why is this change needed?

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
How was this tested?

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Validation passes
- [ ] No breaking changes (or documented)

## Screenshots (if applicable)
Add screenshots here.

## Additional Notes
Any other relevant information.
```

### Review Process

1. Maintainer reviews your PR
2. Feedback and requested changes
3. You address feedback
4. Approval and merge

## Project Structure

```
devpost_compition1/
├── config.py                 # Configuration
├── elasticsearch_client.py   # Search implementation
├── gemini_client.py          # AI integration
├── search_assistant.py       # Main logic
├── cli.py                    # CLI interface
├── index_sample_data.py      # Data utilities
├── example.py                # Usage examples
├── validate.py               # Validation tool
├── demo.py                   # Demo script
├── test_*.py                 # Test files
├── requirements.txt          # Dependencies
├── README.md                 # Main documentation
├── QUICKSTART.md             # Quick start guide
├── ARCHITECTURE.md           # Architecture docs
├── DEPLOYMENT.md             # Deployment guide
└── .github/
    └── workflows/
        └── ci.yml            # CI/CD pipeline
```

## Areas for Contribution

### High Priority

- [ ] Web API (Flask/FastAPI)
- [ ] More comprehensive tests
- [ ] Performance optimizations
- [ ] Multi-language support
- [ ] Query expansion
- [ ] Result caching

### Medium Priority

- [ ] Web UI
- [ ] Advanced filtering
- [ ] Analytics dashboard
- [ ] User authentication
- [ ] Rate limiting
- [ ] API documentation

### Good First Issues

- [ ] Documentation improvements
- [ ] Code examples
- [ ] Bug fixes
- [ ] Test coverage
- [ ] Error message improvements
- [ ] Configuration validation

## Development Workflow

### Feature Development

```bash
# 1. Create branch
git checkout -b feature/my-feature

# 2. Make changes
# ... edit files ...

# 3. Test
python validate.py
python -m unittest discover

# 4. Commit
git add .
git commit -m "Add: brief description"

# 5. Push and create PR
git push origin feature/my-feature
```

### Commit Messages

Follow conventional commits:

- `Add: new feature`
- `Fix: bug description`
- `Update: change description`
- `Remove: removed feature`
- `Refactor: code restructuring`
- `Docs: documentation update`
- `Test: test additions/changes`

## Getting Help

- **Documentation**: Read the docs first
- **Issues**: Search existing issues
- **Discussions**: Ask questions in GitHub Discussions
- **Contact**: Reach out to maintainers

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation

Thank you for contributing! 🎉
