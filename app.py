import os
import requests
import json

# Define global context to store interactions
context = []

# Base URL for Ollama API
OLLAMA_API_BASE = "http://localhost:11434"  # Default port for Ollama

def send_instruction_to_ollama(instruction):
    """Send a user's instruction to the Ollama service and get the response."""
    global context
    try:
        # Include context in the request
        payload = {
            "prompt": "\n".join(context + [instruction])
        }
        response = requests.post(f"{OLLAMA_API_BASE}/generate", json=payload)
        
        if response.status_code == 200:
            result = response.json().get("text", "")
            context.append(f"User: {instruction}")
            context.append(f"AI: {result}")
            return result
        else:
            raise ValueError(f"Failed to get a response: {response.text}")
    except Exception as e:
        return f"Error: {e}"

def load_text_files_from_dir(directory="docs"):
    """Load and display text files from the specified directory."""
    try:
        files = [f for f in os.listdir(directory) if f.endswith(".txt")]
        if not files:
            print("No text files found in the directory.")
            return None

        print("Available text files:")
        for idx, file in enumerate(files):
            print(f"{idx + 1}: {file}")

        choice = int(input("Select a file by number (or 0 to cancel): "))
        if choice == 0:
            return None

        selected_file = os.path.join(directory, files[choice - 1])
        with open(selected_file, "r") as f:
            content = f.read()
        return content
    except Exception as e:
        return f"Error: {e}"

def main():
    """Main CLI loop."""
    print("Welcome to the Ollama CLI tool!")
    print("Type 'exit' to quit, 'context' to view conversation history, or 'load' to load a text file as input.")

    while True:
        user_input = input("\nYour instruction: ").strip()
        
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        elif user_input.lower() == "context":
            print("\nConversation History:")
            print("\n".join(context))
        elif user_input.lower() == "load":
            text = load_text_files_from_dir()
            if text:
                print(f"Loaded text:\n{text}")
                response = send_instruction_to_ollama(text)
                print(f"Ollama Response: {response}")
        else:
            response = send_instruction_to_ollama(user_input)
            print(f"Ollama Response: {response}")

if __name__ == "__main__":
    main()
