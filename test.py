import requests

OMDB_API_KEY = '41e6a6fc'

# Test API call
url = 'http://www.omdbapi.com/'
params = {
    'apikey': OMDB_API_KEY,
    't': 'The Godfather',
    'plot': 'full'
}

response = requests.get(url, params=params)
data = response.json()

if data.get('Response') == 'True':
    print("✅ OMDb API is working!")
    print(f"Title: {data.get('Title')}")
    print(f"Director: {data.get('Director')}")
    print(f"IMDB Rating: {data.get('imdbRating')}")
else:
    print("❌ API Error:", data.get('Error'))