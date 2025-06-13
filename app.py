from flask import Flask, render_template, request
from restaurant_recommender import get_recommendations
 
app = Flask(__name__)
 
# @app.route('/')
# def home():
#     return render_template('index.html')
 
# @app.route('/recommend', methods=['POST'])
# def recommend():
#     name = request.form['restaurant_name']
#     recommendations = get_recommendations(name)
#     return render_template('index.html', name=name, recommendations=recommendations)
 
# if __name__ == '__main__':
#     app.run(debug=True)
 
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    restaurant_name = request.form["restaurant_name"]
    
    # Your recommendation logic here
    recommendations = get_recommendations(restaurant_name)  # Replace with your function

    return render_template("index.html", recommendations=recommendations, name=restaurant_name)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
