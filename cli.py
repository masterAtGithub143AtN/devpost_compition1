"""
Interactive CLI interface for the AI Search Assistant.
"""
import sys
from colorama import init, Fore, Style
from search_assistant import AISearchAssistant
from config import Config

# Initialize colorama for colored terminal output
init(autoreset=True)


def print_banner():
    """Print welcome banner."""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║          AI Search Assistant - Powered by Elastic & Gemini   ║
    ║          Hybrid Search: Semantic + Keyword                   ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(Fore.CYAN + banner)


def print_help():
    """Print help information."""
    help_text = """
    Commands:
        /search <query>  - Perform a hybrid search
        /ask <question>  - Ask a question with AI-powered response
        /chat <message>  - Have a conversation (context-aware)
        /clear           - Clear conversation history
        /history         - Show conversation history
        /help            - Show this help message
        /quit or /exit   - Exit the assistant
    
    You can also just type your message to chat directly.
    """
    print(Fore.YELLOW + help_text)


def print_search_results(results):
    """Print search results in a formatted way."""
    if not results:
        print(Fore.RED + "No results found.")
        return
    
    print(Fore.GREEN + f"\n{len(results)} search results found:\n")
    
    for i, result in enumerate(results, 1):
        print(Fore.CYAN + f"{i}. {result['title']}")
        print(Fore.WHITE + f"   Score: {result['score']:.4f}")
        content = result['content'][:200] + "..." if len(result['content']) > 200 else result['content']
        print(Fore.WHITE + f"   {content}\n")


def main():
    """Main CLI loop."""
    print_banner()
    
    # Initialize assistant
    try:
        assistant = AISearchAssistant()
        print(Fore.GREEN + "✓ AI Search Assistant initialized successfully!\n")
    except Exception as e:
        print(Fore.RED + f"✗ Failed to initialize assistant: {e}")
        print(Fore.YELLOW + "\nMake sure you have:")
        print("  1. Set up Elasticsearch (optional for offline mode)")
        print("  2. Configured your .env file with API keys")
        print("  3. Installed all requirements: pip install -r requirements.txt\n")
        return
    
    print_help()
    
    # Main loop
    while True:
        try:
            # Get user input
            user_input = input(Fore.BLUE + "\nYou: " + Style.RESET_ALL).strip()
            
            if not user_input:
                continue
            
            # Process commands
            if user_input.startswith('/'):
                parts = user_input.split(maxsplit=1)
                command = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ""
                
                if command in ['/quit', '/exit']:
                    print(Fore.CYAN + "Goodbye! 👋")
                    break
                
                elif command == '/help':
                    print_help()
                
                elif command == '/clear':
                    assistant.clear_conversation()
                    print(Fore.GREEN + "✓ Conversation history cleared.")
                
                elif command == '/history':
                    history = assistant.get_conversation_history()
                    if not history:
                        print(Fore.YELLOW + "No conversation history yet.")
                    else:
                        print(Fore.GREEN + "\nConversation History:\n")
                        for msg in history:
                            role = msg['role'].capitalize()
                            content = msg['content']
                            color = Fore.BLUE if msg['role'] == 'user' else Fore.GREEN
                            print(color + f"{role}: {content}\n")
                
                elif command == '/search':
                    if not args:
                        print(Fore.RED + "Please provide a search query.")
                        continue
                    
                    print(Fore.YELLOW + "Searching...")
                    results = assistant.search(args)
                    print_search_results(results)
                
                elif command == '/ask':
                    if not args:
                        print(Fore.RED + "Please provide a question.")
                        continue
                    
                    print(Fore.YELLOW + "Thinking...")
                    result = assistant.ask(args)
                    
                    if result['search_results']:
                        print(Fore.CYAN + "\n[Search Results Used]")
                        print_search_results(result['search_results'])
                    
                    print(Fore.GREEN + "\nAssistant: " + Fore.WHITE + result['response'])
                
                elif command == '/chat':
                    if not args:
                        print(Fore.RED + "Please provide a message.")
                        continue
                    
                    print(Fore.YELLOW + "Thinking...")
                    response = assistant.chat(args)
                    print(Fore.GREEN + "Assistant: " + Fore.WHITE + response)
                
                else:
                    print(Fore.RED + f"Unknown command: {command}")
                    print(Fore.YELLOW + "Type /help for available commands.")
            
            else:
                # Default to chat mode
                print(Fore.YELLOW + "Thinking...")
                response = assistant.chat(user_input)
                print(Fore.GREEN + "Assistant: " + Fore.WHITE + response)
        
        except KeyboardInterrupt:
            print(Fore.CYAN + "\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(Fore.RED + f"Error: {e}")
            continue


if __name__ == "__main__":
    main()
