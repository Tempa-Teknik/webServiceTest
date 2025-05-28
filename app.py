from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)
messages = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/post', methods=['POST'])
def receive_post():
    data = request.get_json(force=True)
    messages.append(data)
    return {'status': 'ok'}

@app.route('/clear', methods=['POST'])
def clear_messages():
    messages.clear()
    return redirect(url_for('index'))

@app.route('/api/messages', methods=['GET'])
def get_messages():
    return {'messages': messages}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
