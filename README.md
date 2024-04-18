# MetaAI

MetaAI is a Python library designed to interact with Meta's AI APIs. It encapsulates the complexities of authentication and communication with the APIs, providing a straightforward interface for sending queries and receiving responses.

With this you can easily prompt the AI with a message and get a response, directly from your Python code. **NO API KEY REQUIRED**

## Usage
1. **Download**:

   ```bash
   pip install meta-ai
   ```
   
2. **Initialization**:

   ```python
   from meta_ai import MetaAI
   
   if __name__ == "__main__":
       ai = MetaAI()
       ai.prompt(message="Whats the weather in San Francisco today?")
   ```
