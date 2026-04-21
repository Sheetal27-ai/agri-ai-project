from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot_logic import get_chatbot_response

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes to allow frontend access

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("msg", "")
    
    if not user_message:
        return jsonify({"response": "I didn't catch that. Could you repeat?"}), 400
    
    # Get response from logic handler
    bot_response = get_chatbot_response(user_message)
    
    return jsonify({"response": bot_response})

if __name__ == '__main__':
    print("AgriVision Pro Chatbot Backend running on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
