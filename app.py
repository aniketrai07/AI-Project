from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Allow all origins for testing

# Configure API key from environment variable
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

@app.route('/api/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '').strip()
    
    if not user_input:
        return jsonify({'response': 'Please enter a message.'}), 400

    try:
        model = genai.GenerativeModel(
            'gemini-2.0-flash',
         system_instruction="You are a friendly fleet management assistant. Respond only to queries related to vehicles, drivers, trips, maintenance, and fleet operations. For unrelated topics or greetings (e.g., 'hi'), acknowledge the user and gently steer the conversation back to fleet management topics. Keep responses concise and professional."
        )
        response = model.generate_content(user_input)
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'response': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
