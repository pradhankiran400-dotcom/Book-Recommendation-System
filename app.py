from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pickle

popular_df = pickle.load(open("popular.pkl", "rb"))

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        request,
        "home.html",
        {
            "request": request,
            "title": "Home Page",
            "book_names": list(popular_df['Book-Title'].values),
            "author_names": list(popular_df['Book-Author'].values),
            "image_urls": list(popular_df['Image-URL-M'].values),
            "votes": list(popular_df['num_ratings'].values),
            "rating": list(popular_df['avg_rating'].values)
        }
    )

@app.get("/recommendations")
def recommend(request: Request):
    return templates.TemplateResponse(
        request,
        "recommendations.html",
        {
            "request": request,
            "title": "Recommendations Page"
        }
    )
