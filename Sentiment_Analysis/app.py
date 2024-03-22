from flask import Flask, render_template, request
import joblib


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analysis", methods=["GET","POST"])
def prediction():
    review = request.form.get("review")
    
    data = str(review)    
    
    model = joblib.load("best_models/logistic_regression.pkl")
    
    prediction = model.predict([data])[0]
    
    if prediction == 'Negative':
        sentiment = 'Negative'
        sentiment_emoji = '😞'
    else:
        sentiment = 'Positive'
        sentiment_emoji = '😊'

    return render_template('result.html',prediction=prediction, review=review, sentiment_emoji=sentiment_emoji)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

