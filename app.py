from flask import Flask, jsonify, render_template

app = Flask(__name__, static_folder='.', template_folder='.')

# Mock database of games
GAMES = [
    {"id": 1, "title": "Cyberpunk 2077", "genre": "RPG", "rating": 4.8, "price": 59.99},
    {"id": 2, "title": "Valorant", "genre": "FPS", "rating": 4.5, "price": 0.00},
    {"id": 3, "title": "Forza Horizon 5", "genre": "Racing", "rating": 4.9, "price": 49.99},
    {"id": 4, "title": "Elden Ring", "genre": "Action RPG", "rating": 5.0, "price": 59.99}
]

@app.route('/')
def index():
    # Serves the index.html file
    return render_template('index.html')

@app.route('/api/games', methods=['GET'])
def get_games():
    # Returns the list of games as JSON
    return jsonify({"success": True, "games": GAMES})

if __name__ == '__main__':
    # Run the app on port 5000
    app.run(debug=True, port=5000)
