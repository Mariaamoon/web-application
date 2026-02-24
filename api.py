from fastapi import FastAPI, Request, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as starletteHTTPpexception
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from schemas import postcreate, postresponse


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

posts: list[dict] = [
    {
        "id": 1,
        "author": "corey schafer",
        "title": "fast api is awesome",
        "content": "this framework is easy",
        "date_posted": "april 20",
    },
    {
        "id": 2,
        "author": " jane doe",
        "title": "python is great for web develpment",
        "content": "python is great for web and easy to use",
        "date_posted": "april 21",
    },
]


@app.get("/", include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False, name="posts")
def home(request: Request):
    return templates.TemplateResponse(
        request, "home.html", {"posts": posts, "title": "home"}
    )


@app.get("/posts/{post_id}", include_in_schema=False)
def post_page(request: Request, post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            title = post["title"][:50]
            return templates.TemplateResponse(
                request, "post.html", {"post": post, "title": title}
            )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="post was not found"
    )


@app.get("/api/posts", response_model=list[postresponse])
def get_posts():
    return posts


@app.post(
    "/api/posts", response_model=postresponse, status_code=status.HTTP_201_CREATED
)
def create_post(post: postcreate):
    new_id = max(p["id"] for p in posts) + 1 if posts else 1
    new_post = {
        "id": new_id,
        "author": post.author,
        "title": post.title,
        "content": post.content,
        "date_posted": "april 20 2025",
    }
    posts.append(new_post)
    return new_post


@app.get("/api/posts/{post_id}", response_model=postresponse)
def get_post(post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            return post
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="post was not found"
    )


@app.exception_handler(starletteHTTPpexception)
def general_http_exception_handler(
    request: Request, exception: starletteHTTPpexception
):
    message = exception.detail if exception.detail else "an error accured"
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail ": message},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail ": exception.errors()},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "invalid request",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )
