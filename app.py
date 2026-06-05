from fastapi import FastAPI, Request
import numpy as np
import gc
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pickle
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from typing import Optional

popular_df = pickle.load(open("popular.pkl", "rb"))
pt = pickle.load(open("pt.pkl", "rb"))
books = pickle.load(open("books.pkl", "rb"))
similarity_scores = pickle.load(open("similarity_scores.pkl", "rb"))

gc.collect()

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
def recommendations_page(request: Request):
    return templates.TemplateResponse(
        request,
        "recommendations.html",
        {
            "request": request,
            "title": "Recommendations Page",
            "data": None
        }
    )

@app.get("/recommend", response_class=HTMLResponse)
def recommend(request: Request, book_name: Optional[str] = None):
    
    if not book_name:
        return templates.TemplateResponse(
            request,
            "recommendations.html", 
            {"request": request, "title": "Recommendations Page", "data": None}
        )
        
    try:
        index = np.where(pt.index == book_name)[0][0]
        distances = similarity_scores[index]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]
        
        data = []
        for i in similar_items:
            items = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            items.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            items.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            items.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
            data.append(items)
            
        return templates.TemplateResponse(
            request,
            "recommendations.html",
            {"request": request,
              "title": "Recommendations Page",
             "data": data
            }
        )
        
    except IndexError:
        return templates.TemplateResponse(
            request,
            "recommendations.html",
            {"request": request,
              "title": "Recommendations Page",
              "data": None, "error": "Book not found!"
            }
        )

@app.get("/about")
def about(request: Request):
    return templates.TemplateResponse(
        request,
        "about.html",
        {"request": request, "title": "About Page"}
    )

@app.get("/suggest-books")
def suggest_books(q: str = ""):
    if not q or len(q) < 2:  
        return JSONResponse([])
    
    query = q.lower()
    all_books = pt.index.tolist() 
    
    
    suggestions = [book for book in all_books if query in book.lower()][:8]
    
    return JSONResponse(suggestions)

@app.exception_handler(StarletteHTTPException)
def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        message = "The page you are looking for does not exist."
    elif exc.status_code == 500:
        message = "An internal server error occurred."
    else:
        message = exc.detail if exc.detail else "An error occurred while processing your request."     

    return templates.TemplateResponse(
        request,
        "404.html",
        {
            "request": request,
            "status_code": exc.status_code,
            "title": f"Error {exc.status_code}",
            "message": message
        },
        status_code=exc.status_code, 
    )