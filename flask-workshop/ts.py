from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/username/')
def username():
    return render_template('username.html')

@app.route('/hashtag/')
def hashtag():
    return render_template('hashtag.html')

@app.route('/about/')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run()
