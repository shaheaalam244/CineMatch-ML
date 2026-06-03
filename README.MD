# CineMatch 🎬

CineMatch is a blazing fast, Machine Learning-powered recommendation engine designed to suggest movies, Bollywood hits, and Web Series tailored to your taste. Built specifically to deliver personalized recommendations using Natural Language Processing (NLP) techniques.

## 🚀 Key Features

- **Smart Recommendations:** Uses machine learning algorithms to compare movie plots and genres to find the perfect match.
- **Lightning Fast Performance:** Employs `ThreadPoolExecutor` for parallel API requests and `@lru_cache` for memory caching, making the app 10x faster.
- **Multiple Categories:** Explore dedicated sections for Hollywood, Bollywood, and Web Series.
- **Real-Time Search & Filtering:** Filter movies instantly by genre, minimum rating, and category.
- **Beautiful UI:** Responsive, modern design with a sleek dark mode interface.

## 🛠️ Technologies & Libraries Used

### Backend Framework
- **Python 3.x**
- **Flask**: The core web framework used to serve the application and handle routing.

### Data Science & Machine Learning
- **Pandas**: Used for loading, cleaning, and managing the large movie datasets efficiently.
- **Scikit-Learn**: The heart of the recommendation engine. 
  - `TfidfVectorizer`: Converts movie plots (text) into numerical features (vectors) based on term frequency-inverse document frequency.
  - `cosine_similarity`: Calculates the similarity score between different movie vectors to find the closest matches.

### APIs & Networking
- **OMDb API / TMDB**: Fetches real-time movie posters, ratings, cast, and director information.
- **Requests**: For handling HTTP API calls.
- **Concurrent.futures (ThreadPoolExecutor)**: Handles parallel fetching of movie posters to drastically reduce page load times.

### Frontend
- **HTML5 & CSS3**
- **Bootstrap 5**: For responsive layout and pre-built components.
- **FontAwesome**: For beautiful icons used throughout the interface.
- **Jinja2**: Templating engine used by Flask to render HTML dynamically.

## 🧠 How the Recommendation Works

1. **Text Vectorization**: When you select a movie, the system looks at its `overview` (story) and `genre`. It uses `TfidfVectorizer` to convert this text into mathematical vectors.
2. **Similarity Scoring**: It then uses `Cosine Similarity` to measure the angle between the vector of your selected movie and all other movies in the dataset.
3. **Ranking**: The movies with the highest similarity scores (closest matches in storyline and genre) are ranked and the top 8 are returned instantly.
4. **Caching**: Once a calculation is done, it is saved in memory (`@lru_cache`). If someone searches the same movie again, it loads in 0.01 seconds!

## ⚙️ Setup and Installation

Follow these steps to run the project on your local machine:

**1. Clone the repository / Navigate to the folder**
```bash
cd Movie-Recomendation-master
```

**2. Create a Virtual Environment**
It's highly recommended to use a virtual environment to manage dependencies.
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the Application**
```bash
python app.py
```

**5. Open in Browser**
Navigate to `http://127.0.0.1:5001` in your web browser.

## 📂 Project Structure

```
CineMatch/
├── app.py                # Main Flask application and ML logic
├── requirements.txt      # Python dependencies
├── dataset.csv           # Hollywood movies dataset
├── bollywood.csv         # Bollywood movies dataset
├── webseries.csv         # Web Series dataset
├── templates/            # HTML templates (Jinja2)
│   ├── base.html         # Main layout wrapper
│   ├── index.html        # Home page
│   ├── movie_detail.html # Movie recommendation page
│   └── ...               
└── static/               # CSS, JS, and image assets
```

---
*Developed by **Shahe Aalam***
