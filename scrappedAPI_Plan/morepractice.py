import requests
import json

def jprint(obj): 
    text = json.dumps(obj, indent=4)
    print(text)

api_url = "https://api.nytimes.com/svc/books/v3/lists/best-sellers/history.json?api-key=R9RSHuxrGmLLXRwgPCV11WGa1huyK6iA"

response = requests.get(api_url)

page_results = response.json()['results']

home_books = []

for books in page_results:
    book_data = {
            'title': books['title'],
            'author': books['author'],
            'description': books['description'],
            'publisher': books['publisher'],
            # 'isbns': books['isbns'][0]['isbn10']
            'isbn': books['isbns'][0]['isbn10'] if len(books['isbns']) > 0 else None
            }
    home_books.append(book_data)
jprint(home_books)

# jprint(response.json())