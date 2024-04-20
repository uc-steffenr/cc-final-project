from flask import Flask, render_template, request

app = Flask(
    __name__,
    template_folder='templates',
    static_folder='static'
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/next')
def to_next():
    return render_template('next.html')

if __name__ == '__main__':
    # Run Flask app
    app.run(host='0.0.0.0', debug=True, port=8080)

