# Book Recommendation System 📚

A sleek, modern, and fully responsive web application built using **FastAPI** and **Python** that displays top-rated books and provides personalized book recommendations.

## ✨ Features
* **Top 50 Books Display:** Dynamically renders the highest-rated books fetched from a curated dataset via Pandas and Pickle.
* **Responsive Navbar:** Clean, fluid navigation layout that adjusts smoothly across mobile, tablet, and desktop screens.
* **Animated UI Elements:** Custom interactive cards featuring hovering scale effects and a neon-gradient spinning border animation.
* **Graceful Degradation:** Automatic replacement handling (`onerror`) for broken or missing book cover image links using a default placeholder.
* **Custom Error Pages:** Integrated global 404 route handling to redirect users back to safety when a page is not found.

## 🛠️ Tech Stack
* **Backend:** Python, FastAPI, Uvicorn, Jinja2 Templates
* **Data Processing:** Pandas, Pickle
* **Frontend:** HTML5, CSS3 (Flexbox, Media Queries, Keyframe Animations)

## 📁 Project Structure
```text
BOOK-RECOMMENDOR/
├── static/
│   ├── CSS/
│   │   └── style.css
│   └── js/
│       └── app.js
├── templates/
│   ├── 404.html
│   └── home.html
├── venv/
├── app.py
├── model.py
├── popular_df.pkl
└── requirements.txt
