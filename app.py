from flask import Flask, render_template
import requests
import config # นำเข้าไฟล์ config.py

# --- ตั้งค่า ---
# อ่านค่า API Key มาจากไฟล์ config.py
API_KEY = config.TMDB_API_KEY 

# ฟังก์ชันสำหรับดึงข้อมูลหนังจาก TMDB
def get_movies(endpoint):
    url = f"https://api.themoviedb.org/3/{endpoint}"
    params = {'api_key': API_KEY, 'language': 'th-TH'}
    response = requests.get(url, params=params)
    data = response.json()
    return data.get('results', [])

# ฟังก์ชันสำหรับดึงข้อมูลหนังแค่เรื่องเดียว
def get_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {'api_key': API_KEY, 'language': 'th-TH'}
    response = requests.get(url, params=params)
    return response.json()

app = Flask(__name__)

@app.route('/')
def home():
    movie_categories = {
        "Popular": get_movies("movie/popular"),
        "Top Rated": get_movies("movie/top_rated"),
        "Upcoming": get_movies("movie/upcoming")
    }
    return render_template('index.html', categories=movie_categories)

# Route ใหม่สำหรับหน้ารายละเอียดหนัง
@app.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    details = get_movie_details(movie_id)
    return render_template('details.html', movie=details)

if __name__ == '__main__':
    app.run(debug=True)