from flask import Flask, Blueprint, request, jsonify
from flask_cors import CORS
import model.laptop.chatbot as bot

def create_app():
    app = Flask(__name__)

    # Define a blueprint for the laptop consulting API
    laptop_consulting_api_v1 = Blueprint('laptop_consulting_api_v1', 'laptop_consulting_api_v1', url_prefix='/api/laptop-consulting')

    # Enable CORS for the laptop consulting API
    CORS(laptop_consulting_api_v1)

    # Define the API endpoint for answering laptop consulting messages
    @laptop_consulting_api_v1.route('/message', methods=['POST'])
    def message():
        try:
            data = request.get_json()
            answer_message = bot.answer(data["message"])

            return jsonify({'success': True, 'message': answer_message})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 400

    # Register the laptop consulting API blueprint
    app.register_blueprint(blueprint=laptop_consulting_api_v1)

    return app

if __name__ == "__main__":
    app = create_app()
    # Enable CORS
    CORS(app)
    # Enable debug mode
    app.config['DEBUG'] = True
    app.run()
