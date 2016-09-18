from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/index.html")
def index():
    return render_template("index.html")



@app.route("/patrollers.html")
def update_patrollers():
    return render_template("patrollers.html")


if __name__ == "__main__":
    app.run()
