# MetaAI API Wrapper

MetaAI is a Python library designed to interact with Meta's AI APIs that run in the backend of https://www.meta.ai/. It encapsulates the complexities of authentication and communication with the APIs, providing a straightforward interface for sending queries and receiving responses.

With this you can easily prompt the AI with a message and get a response, directly from your Python code. **NO API KEY REQUIRED**

**Meta AI is connected to the internet, so you will be able to get the latest real-time responses from the AI.** (powered by Bing)

Meta AI is running Llama 3 LLM.

## Usage
1. **Download**:

   ```bash
   pip install meta-ai-api
   ```
   
2. **Initialization**:

   ```python
    from meta_ai_api import MetaAI
   
    if __name__ == "__main__":
        ai = MetaAI()
        response = ai.prompt(message="Whats the weather in San Francisco today? And what is the date?")
        print(response)
    
        # Today's weather in San Francisco, CA, on Thursday, April 18, 2024, is mostly sunny
        # and not as warm, with a high of 71 degrees Fahrenheit and a low of 51 degrees Fahrenheit ¹.
        # The wind is coming from the west-southwest direction at a speed between 8 and 10 miles per hour,
        # and the chance of precipitation is 25% ².
    
        response = ai.prompt(message="What was the Warriors score last game?")
        print(response)
    
        # The Golden State Warriors' last game was against the Sacramento Kings on April 16, 2024,
        # at the Golden 1 Center, in which they lost 118-94 ¹ ². Here are some additional details about the game ¹:
        # Venue: Golden 1 Center, Sacramento, USA
        # Kings (SAC): 118 points
        # Warriors (GSW): 94 points
        # Quarter 1: Kings 31, Warriors 22
        # Quarter 2: Kings 23, Warriors 28
        # Quarter 3: Kings 37, Warriors 26
        # Quarter 4: Kings 27, Warriors 18
    ```
