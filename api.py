from fastapi import FastAPI,Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app=FastAPI()

app.mount("/static",StaticFiles(directory="static"),name="static")
templates = Jinja2Templates(directory= "templates")

posts: list[dict] = [

{ 
    "id" : 1,
    "author" : "corey schafer" ,
    "title" : "fast api is awesome",
    "content" : "this framework is easy",
    "date_posted" : "april 20",
},
{
    "id" : 2,
    "author" : " jane doe",
    "title" : "python is great for web develpment",
    "content" : "python is great for web and easy to use",
    "date_posted" : "april 21",
},
]



@app.get('/'  ,include_in_schema=False,name="home")
@app.get('/posts' ,include_in_schema=False,name="posts")
def home(request : Request):
    return templates.TemplateResponse(request,"home.html",{"posts" : posts , "title" :"home"})

@app.get('/api/posts')
def get_posts():
    return posts

