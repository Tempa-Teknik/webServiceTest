from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

messages = []  # Gelen mesajları burada tutuyoruz

@app.route('/')
def index():
    return render_template('index.html', messages=messages)

@app.route('/Api/indicatorapi/milk-delivery/<string:user_id>', methods=['POST'])
def milk_delivery(user_id):
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'Geçerli JSON gönderiniz'}), 400

    message = {
        'user_id': user_id,
        'data': data
    }
    messages.append(message)

    return jsonify({'status': 'success', 'received': message})

@app.route('/clear_messages', methods=['POST'])
def clear_messages():
    messages.clear()
    return '', 204

@app.route('/get_messages')
def get_messages():
    return jsonify({'messages': messages})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
