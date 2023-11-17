from flask import Flask, render_template

app = Flask(__name__)

# Sample data or your previous script output
previous_script_output = "This is the output of our previous script."

@app.route('/')
def index():
    return render_template('index.html', output=previous_script_output)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
