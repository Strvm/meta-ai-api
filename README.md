# MetaAI API Wrapper

MetaAI is a Python library designed to interact with Meta's AI APIs that run in the backend of https://www.meta.ai/. It encapsulates the complexities of authentication and communication with the APIs, providing a straightforward interface for sending queries and receiving responses.

With this you can easily prompt the AI with a message and get a response, directly from your Python code. **NO API KEY REQUIRED**

**Meta AI is connected to the internet, so you will be able to get the latest real-time responses from the AI.** (powered by Bing)

Meta AI is running Llama 3 LLM.

## Features
- **Prompt AI**: Send a message to the AI and get a response from Llama 3.
- **Image Generation**: Generate images using the AI. (Only for FB authenticated users)
- **Get Up To Date Information**: Get the latest information from the AI thanks to its connection to the internet.
- **Get Sources**: Get the sources of the information provided by the AI.
- **Streaming**: Stream the AI's response in real-time or get the final response.
- **Follow Conversations**: Start a new conversation or follow up on an existing one.

## Usage
**Download**:

   ```bash
   pip install meta-ai-api
   ```
   
**Initialization**:

```python
from meta_ai_api import MetaAI

ai = MetaAI()
response = ai.prompt(message="Whats the weather in San Francisco today? And what is the date?")
print(response)
 
```
```json
{
   "message":"The weather in San Francisco today is mostly clear to overcast, with no precipitation, a wind speed between 0 and 8 miles per hour and temperatures ranging from 51 to 55 degrees Fahrenheit ¹. The date is Friday, April 19, 2024 ². Please note that the weather forecast is continually changing ³ ⁴ ⁵ ⁶.\n",
   "sources":[
      {
         "link":"https://www.wolframalpha.com/input?i=San+Francisco+weather+today+and+date",
         "title":"WolframAlpha"
      },
      {
         "link":"https://www.timeanddate.com/weather/usa/san-francisco",
         "title":"Weather for San Francisco, California, USA - timeanddate.com"
      },
      {
         "link":"https://www.accuweather.com/en/us/san-francisco/94103/weather-today/347629",
         "title":"Weather Today for San Francisco, CA | AccuWeather"
      },
      {
         "link":"https://www.accuweather.com/en/us/san-francisco/94103/weather-forecast/347629",
         "title":"San Francisco, CA Weather Forecast | AccuWeather"
      },
      {
         "link":"https://forecast.weather.gov/zipcity.php?inputstring=San%20francisco%2CCA",
         "title":"National Weather Service"
      },
      {
         "link":"https://www.wunderground.com/weather/us/ca/san-francisco",
         "title":"San Francisco, CA Weather Conditions | Weather Underground"
      }
   ]
}
```
---
### Follow conversations:
```python
```python
meta = MetaAI()

print(meta.prompt("what is 2 + 2?"))
print(meta.prompt("what was my previous question?"))
```

```
{'message': '2 + 2 = 4\n', 'sources': [], 'media': []}
{'message': 'Your previous question was "what is 2 + 2?"\n', 'sources': [], 'media': []}
```

And to start a new one:
```python
meta = MetaAI()

print(meta.prompt("what is 2 + 2?"))
print(meta.prompt("what was my previous question?", new_conversation=True))
```

```
{'message': '2 + 2 = 4\n', 'sources': [], 'media': []}
{'message': "This is the beginning of our conversation, so I don't have a previous question to refer to. I'm happy to chat with you, though! What's on your mind today?\n", 'sources': [], 'media': []}
```

---
```python
from meta_ai_api import MetaAI

ai = MetaAI()
response = ai.prompt(message="What was the Warriors score last game?")
print(response)
```
```json
{
   "message":"The Golden State Warriors' last game was against the Sacramento Kings, and they lost 118-94 ¹ ². Stephen Curry scored 22 points, and the Kings' win eliminated the Warriors from the playoffs ³. The Warriors finished the season 46-36 and 10th in the Western Conference ⁴ ³.\n",
   "sources":[
      {
         "link":"https://sportradar.com/",
         "title":"Game Info of NBA from sportradar.com"
      },
      {
         "link":"https://www.sofascore.com/team/basketball/golden-state-warriors/3428",
         "title":"Golden State Warriors live scores & schedule - Sofascore"
      },
      {
         "link":"https://www.foxsports.com/nba/golden-state-warriors-team-schedule",
         "title":"Golden State Warriors Schedule & Scores - NBA - FOX Sports"
      },
      {
         "link":"https://en.wikipedia.org/wiki/History_of_the_Golden_State_Warriors",
         "title":"History of the Golden State Warriors"
      }
   ]
}
```

**Using proxy**:

```python
from meta_ai_api import MetaAI

proxy = {
    'http': 'http://proxy_address:port',
    'https': 'https://proxy_address:port'
}

ai = MetaAI(proxy=proxy)
response = ai.prompt(message="How to find out which mushrooms are edible?")
print(response)
```

**Streaming Response**:

```python
from meta_ai_api import MetaAI

ai = MetaAI()
response = ai.prompt(message="What was the Warriors score last game?", stream=True)
for r in response:
    print(r)
```

```
{'message': '\n', 'sources': []}
{'message': 'The\n', 'sources': []}
{'message': 'The Golden\n', 'sources': []}
{'message': 'The Golden State\n', 'sources': []}
{'message': 'The Golden State Warriors\n', 'sources': []}
{'message': "The Golden State Warriors'\n", 'sources': []}
{'message': "The Golden State Warriors' last\n", 'sources': []}
{'message': "The Golden State Warriors' last game\n", 'sources': []}
{'message': "The Golden State Warriors' last game was\n", 'sources': []}
{'message': "The Golden State Warriors' last game was against\n", 'sources': []}
{'message': "The Golden State Warriors' last game was against the\n", 'sources': []}
{'message': "The Golden State Warriors' last game was against the Sacramento\n", 'sources': []}
{'message': "The Golden State Warriors' last game was against the Sacramento Kings\n", 'sources': []}
{'message': "The Golden State Warriors' last game was against the Sacramento Kings on\n", 'sources': []}
{'message': "The Golden State Warriors' last game was against the Sacramento Kings on April\n", 'sources': []}
...
{'message': "The Golden State Warriors' last game was against the Sacramento Kings on April 16, 2024, at the Golden 1 Center in Sacramento, California. The Kings won the game with a score of 118-94, with the Warriors scoring 22 points in the first quarter, 28 in the second, 26 in the third and 18 in the fourth quarter ¹.\n", 'sources': [{'link': 'https://sportradar.com/', 'title': 'Game Info of NBA from sportradar.com'}]}
```

**Generate Image**:

By default image generation is only available for FB authenticated users. If you go on https://www.meta.ai/ , and ask the AI to generate an image, you will be prompted to authenticate with Facebook.
So if you want to generate images using this library, you need to authenticate using your FB credentials.

**Note**: There seems to be higher rate limits for authenticated users. So only authenticate to generate images.

```python
from meta_ai_api import MetaAI
ai = MetaAI(fb_email="your_fb_email", fb_password="your_fb_password")
resp = ai.prompt(message="Generate an image of a tech CEO")
print(resp)
```

```json
{
   "message":"\n",
   "sources":[
      
   ],
   "media":[
      {
         "url":"https://scontent-lax3-1.xx.fbcdn.net/o1/v/t0/f1/m247/4282108942387920518_1946149595_21-04-2024-14-17-48.jpeg?_nc_ht=scontent-lax3-1.xx.fbcdn.net&_nc_cat=103&ccb=9-4&oh=00_AfCnbCX7nl_J5kF6mahnams4d99Rs5WZA780HGS_scfc6A&oe=662771EE&_nc_sid=5b3566",
         "type":"IMAGE",
         "prompt":"a tech CEO"
      },
      {
         "url":"https://scontent-lax3-1.xx.fbcdn.net/o1/v/t0/f1/m247/3356467762794691754_1025991308_21-04-2024-14-17-48.jpeg?_nc_ht=scontent-lax3-1.xx.fbcdn.net&_nc_cat=108&ccb=9-4&oh=00_AfBLmSbTSqshNAL82KIFk8hGXyL8iK_CZLGcMmmddPrxuA&oe=66276EDD&_nc_sid=5b3566",
         "type":"IMAGE",
         "prompt":"a tech CEO"
      },
      {
         "url":"https://scontent-lax3-1.xx.fbcdn.net/o1/v/t0/f1/m247/127487551948523111_2181921077_21-04-2024-14-17-48.jpeg?_nc_ht=scontent-lax3-1.xx.fbcdn.net&_nc_cat=104&ccb=9-4&oh=00_AfAejXKeKPA4vyKXoc6UR0rEirvZwi41P3KiCSQmHRHsEw&oe=66276E45&_nc_sid=5b3566",
         "type":"IMAGE",
         "prompt":"a tech CEO"
      },
      {
         "url":"https://scontent-lax3-1.xx.fbcdn.net/o1/v/t0/f1/m247/3497663176351797954_3954783377_21-04-2024-14-17-47.jpeg?_nc_ht=scontent-lax3-1.xx.fbcdn.net&_nc_cat=110&ccb=9-4&oh=00_AfBp3bAfcuofqtI-z9D4bHw-GuGgCNPH_xhMM0PG_95S9Q&oe=66277AE9&_nc_sid=5b3566",
         "type":"IMAGE",
         "prompt":"a tech CEO"
      }
   ]
}
```
![Tech CEO](https://i.imgur.com/9YR6qHq.jpeg)

# Educational Purpose:
This repository is intended for educational purposes only. It is a tool to demonstrate how to interact with Meta's AI APIs, providing an example for learning and experimentation. Users should adhere to Meta's terms of service and use the library responsibly.


# Copyright:
This program is licensed under the GNU GPL v3. All code has been written by me, Strvm.

# Copyright Notice:
```
Strvm/meta-ai-api: a reverse engineered API wrapper for MetaAI
Copyright (C) 2023 Strvm

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```

# Meta Copyright:

For more information related to the license tied to Llama, please visit https://www.llama.com/llama3/license/
