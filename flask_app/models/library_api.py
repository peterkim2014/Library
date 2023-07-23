import requests

api_url = "https://api.nytimes.com/svc/books/v3/lists/best-sellers/history.json?api-key=R9RSHuxrGmLLXRwgPCV11WGa1huyK6iA/"

class Book: 

    #GET ALL/DEFAULT 
    def get_all(cls):
        response = requests.get(api_url)
        home_books = []
        for books in response:
            book_data = {
                'id': response['isbn10'],
                'title': response['title']
            }
            home_books.append(book_data)
        print(home_books)


author = "Dana Simpson"

response = requests.get(f"https://api.nytimes.com/svc/books/v3/lists/best-sellers/history.json?api-key=R9RSHuxrGmLLXRwgPCV11WGa1huyK6iA&author=" + author)

results = response.json()['results']

all_titles = []

for books in results: 
    results = books['title']
    all_titles.append(results)
print("Book Titles")
print(all_titles)

# print(response)
# data = response.json()

# print(type(response.json()))
# print(response.json())