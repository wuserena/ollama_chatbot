import requests
from googleapiclient.discovery import build

def get_current_date():

    return print("5/1/2025")

def get_current_weather(city):
    return f"The weather in {city} is sunny."

def get_local_time(city):
    return f"The local time in {city} is 3:00 PM."


def get_weather(city_name):
    #  Open-Meteo
    # https://chatgpt.com/share/6814f682-1098-8011-9e9a-18ca6da9a973
    lat, lon = get_coordinates(city_name)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
        "daily": "temperature_2m_max,temperature_2m_min",
        "timezone": "auto"
    }
    response = requests.get(url, params=params)
    data = response.json()

    current = data.get("current_weather", {})
    print(f"\nCurrent Weather:")
    print(f"  Temperature: {current.get('temperature')}°C")
    print(f"  Wind Speed: {current.get('windspeed')} km/h")

    print("\nForecast:")
    for date, tmax, tmin in zip(data["daily"]["time"], data["daily"]["temperature_2m_max"], data["daily"]["temperature_2m_min"]):
        print(f"  {date}: High {tmax}°C, Low {tmin}°C")
    # Example usage
    # get_weather("New York")
    

def get_coordinates(city_name):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": city_name,
        "format": "json",
        "limit": 1
    }
    response = requests.get(url, params=params, headers={"User-Agent": "weather-script"})
    data = response.json()
    if data:
        lat = float(data[0]["lat"])
        lon = float(data[0]["lon"])
        return lat, lon
    else:
        raise ValueError("City not found")



def save_preference(summary):
    summary

def calendar():
    # https://developers.google.com/workspace/calendar/api/quickstart/python
    # Save reminder or event (sync calendar) / Remind patient of tasks or events (from calendar)

    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    service = build('calendar', 'v3', credentials=creds)

    # Feature 1: List all calendars
    print("Fetching all calendars:")
    calendar_list = service.calendarList().list().execute().get('items', [])
    for calendar in calendar_list:
        print(calendar['summary'])


def contact():
    # Contact care team, emergency contact, or hotline
    contact_list = []

def pull_personal_information():
    # Pull out information from previously saved medical history or preferences


def google_search(query, num_results=5):
    # Search web at patient’s request
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': query,
        'key': api_key,
        'cx': cse_id,
        'num': num_results
    }
    response = requests.get(url, params=params)
    results = response.json()
    
    for i, item in enumerate(results.get("items", []), start=1):
        print(f"{i}. {item['title']}")
        print(f"   {item['link']}")
        print(f"   {item.get('snippet', '')}\n")

    # Replace these with your actual API key and CSE ID
    API_KEY = 'YOUR_API_KEY'
    CSE_ID = 'YOUR_SEARCH_ENGINE_ID'

    # Example usage
    #google_search("Temple University AI lab", API_KEY, CSE_ID)
