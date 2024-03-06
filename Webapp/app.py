from flask import Flask, request, render_template
from your_regex_file import regex

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("home.html")
    if request.method == "POST":
        input_string = request.form["Input_String"]
        pattern = request.form["Test_String"]  
        matches = regex(input_string, pattern)
        return render_template("home.html", input_string=input_string, pattern=pattern, matches=matches)
    return render_template("home.html")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port = 5000)
