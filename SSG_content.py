import csv
import random
from urllib import request
import json
import datetime
import requests

"""
Retrieve an english idioms from an attached csv file 
"""
def get_random_quote(quote_file = "SSG_quotes.csv"):
    try: 
       with open(quote_file, 'r') as f: 
           quotes = [{'saying': line[0],
                      'meaning': line[1]} for line in csv.reader(f, delimiter='|')]

    except Exception as e: # if error occurs, this below default quote will be used
        quotes = [{'saying': 'A blessing in disguise',
                   'meaning': 'A good thing that seemed bad at first'}]
    
    return random.choice(quotes)

"""
Retrieve the current weather forecast from OpenWeatherMap, their API is free.
"""
def get_weather_forecast(coords={'lat': 37.3394, 'lon': -121.895}): #default location is san jose
    try: 
        api_key = ' ' # replace with your own OpenWeatherMap API key
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={coords['lat']}&lon={coords['lon']}&appid={api_key}&units=metric'
        data = json.load(request.urlopen(url))

       
        forecast = {'city': data['name'],
                    'country': data['sys']['country'],
                    'temp': round(data['main']['temp']),
                    'weather': data['weather'][0]['description'],
                    'time': datetime.datetime.fromtimestamp(data['dt']),
                    }

    
        return forecast

    except Exception as e:
        print(e)        

"""
Retrieve main news for the day from worldnews, API is free.
"""

def my_custom_function():
    try:
        url = "https://api.worldnewsapi.com/top-news?source-country=us&language=en&date=2025-04-15"
        api_key = " " # replace with your own API key

        headers = {'x-api-key': api_key}

        response = requests.get(url, headers=headers)
        data = response.json()

        top_news = { 'language': data['language'],
                     'country': data['country'],
                     'articles': list(),}
    
        for i in range (0,9):
            top_news['articles'].append({'title': data['top_news'][i]['news'][0]['title'],
                                          'url': data['top_news'][i]['news'][0]['url']})

        
        return top_news


    except Exception as e:
        print (f"Error: {response.status_code}")

"""
Retrieve a random wikipedia article
"""

def get_wikipedia_article():
    try: 
        url = 'https://en.wikipedia.org/api/rest_v1/page/random/summary'
        response = requests.get(url)
        data = response.json()

        return { 'title': data['title'],
                         'description': data['description'],
                         'extract': data['extract'],
                        'url': data['content_urls']['desktop']['page']
                         }
        

    except Exception as e:
        print(e)
        

if __name__ == '__main__':
   # idioms retrieval
    print('\nTesting idioms...')

    daily_quote = get_random_quote()
    print(f' - Saying of the day is "{daily_quote["saying"]}" - {daily_quote["meaning"]}')
    
    daily_quote = get_random_quote(quote_file = None)
    print(f' - Default saying is "{daily_quote["saying"]}" - {daily_quote["meaning"]}')



    # weather forecast
    print('\nTesting weather forecast retrieval...')

    forecast = get_weather_forecast() # get forecast for default location San Jose
    if forecast:
    
        print(f' The forecast for {forecast['city']}, {forecast['country']} on {forecast['time']} is:')
        print (f'    {forecast['temp']}°C   with     {forecast ['weather']}')

    mulund = {'lat': 19.0144,'lon': 72.8479} # coordinates for Mumbai, Mulund
    forecast = get_weather_forecast(coords = mulund) 
    if forecast:
        print(f' The forecast for {forecast['city']}, {forecast['country']} on {forecast['time']} is:')
        print (f'    {forecast['temp']}°C  with     {forecast ['weather']}')
        
        

    invalid = {'lat': 1234.5678 ,'lon': 1234.5678} # invalid coordinates
    forecast = get_weather_forecast(coords = invalid) # get forecast for invalid location
    if forecast is None:
        print('Weather forecast for invalid coordinates returned None')


    # TOP NEWS
    print('\nTop news are...')

    top_news = my_custom_function()
    if top_news:
        for items in top_news['articles']:
            print(f'{items['title']} \n < {items['url']}>\n')

    # retrieval of wikipedia article
    print('\nTesting random Wikipedia article retrieval...')

    article = get_wikipedia_article()
    if article:
        print(f'\n{article["title"]}\n<{article["url"]}>\n{article["extract"]}')