# MetaAI API Wrapper

MetaAI is a Python library designed to interact with Meta's AI APIs that run in the backend of https://www.meta.ai/. It encapsulates the complexities of authentication and communication with the APIs, providing a straightforward interface for sending queries and receiving responses.

With this you can easily prompt the AI with a message and get a response, directly from your Python code. **NO API KEY REQUIRED**

**Meta AI is connected to the internet, so you will be able to get the latest real-time responses from the AI.** (powered by Bing)

Meta AI is running Llama 3 LLM.

## Features
- **Prompt AI**: Send a message to the AI and get a response from Llama 3.
- **Get Up To Date Information**: Get the latest information from the AI thanks to its connection to the internet.
- **Get Sources**: Get the sources of the information provided by the AI.

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
result:
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

```python
from meta_ai_api import MetaAI

ai = MetaAI()
response = ai.prompt(message="What was the Warriors score last game?")
print(response)
```
result:
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
