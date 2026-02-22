from fastapi import FastAPI
from fastapi.responses import HTMLResponse

posts: list[dict] = [

{ 
    "id" : 1,
    "author" : "corey schafer" ,
    "title" : "fast api is aawesome",
    "contenct" : "this framework is easy",
    "date" : "apri; 20",
},
{
    "id" : 2,
    "author" : " jane doe",
    "title" : "python is great for web develpment",
    "content" : "python is great for web and easy to use",
    "date" : "april 21",
},
]

app=FastAPI()

@app.get('/' ,response_class= HTMLResponse,include_in_schema=False)
@app.get('/posts' ,response_class= HTMLResponse,include_in_schema=False)

def home():
    return f"<h1> {posts[0]['title']}<h1>"

@app.get('/api/posts')
def get_posts():
    return posts

