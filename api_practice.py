import requests
import json


  
# requestUrl = "https://api.nytimes.com/svc/books/v3/lists/best-sellers/history.json?api-key=R9RSHuxrGmLLXRwgPCV11WGa1huyK6iA"
  
# requestHeaders = {
#     "Accept": "application/json"
#   }

# response = requests.get(requestUrl, headers=requestHeaders)

def jprint(obj):
    text = json.dumps(obj, indent=4)
    print(text)

response2 = requests.get("https://api.nytimes.com/svc/books/v3/lists/best-sellers/history.json?api-key=R9RSHuxrGmLLXRwgPCV11WGa1huyK6iA&author=Dana%Simpson")

# response = requests.get("https://api.nytimes.com/svc/books/v3/lists/best-sellers/history.json?api-key=R9RSHuxrGmLLXRwgPCV11WGa1huyK6iA")

titles = response2.json()['results']
# jprint(titles)

all_titles = []

for all_books in titles: 
    results = all_books['title']
    all_titles.append(results)

print(all_titles)


# print(response2.status_code)

jprint(response2.json())
