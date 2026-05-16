from flask import Flask, request, jsonify
from flask_cors import CORS
from config import config
from database import init_db
from ai_agent import AIAgent
from message_handlers import WhatsAppHandler, InstagramHandler, MessengerHandler
import logging
import os
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(config[os.getenv('ENVIRONMENT', 'development')])
CORS(app)

# Initialize database
try:
    init_db()
    logger.info("Database initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize database: {str(e)}")

# Initialize handlers
ai_agent = AIAgent()
whatsapp_handler = WhatsAppHandler(ai_agent)
instagram_handler = InstagramHandler(ai_agent)
messenger_handler = MessengerHandler(ai_agent)

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'MPPRS AI Agent',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    }), 200

# WhatsApp Routes
@app.route('/webhook/whatsapp', methods=['GET'])
def whatsapp_verify():
    """Verify WhatsApp webhook"""
    return whatsapp_handler.verify_webhook(request)

@app.route('/webhook/whatsapp', methods=['POST'])
def whatsapp_webhook():
    """Handle WhatsApp messages"""
    try:
        data = request.get_json()
        logger.info(f"Received WhatsApp message: {data}")
        response = whatsapp_handler.handle_message(data)
        return jsonify(response), 200
    except Exception as e:
        logger.error(f"Error handling WhatsApp message: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Instagram Routes
@app.route('/webhook/instagram', methods=['GET'])
def instagram_verify():
    """Verify Instagram webhook"""
    return instagram_handler.verify_webhook(request)

@app.route('/webhook/instagram', methods=['POST'])
def instagram_webhook():
    """Handle Instagram messages"""
    try:
        data = request.get_json()
        logger.info(f"Received Instagram message: {data}")
        response = instagram_handler.handle_message(data)
        return jsonify(response), 200
    except Exception as e:
        logger.error(f"Error handling Instagram message: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Facebook Messenger Routes
@app.route('/webhook/messenger', methods=['GET'])
def messenger_verify():
    """Verify Messenger webhook"""
    return messenger_handler.verify_webhook(request)

@app.route('/webhook/messenger', methods=['POST'])
def messenger_webhook():
    """Handle Messenger messages"""
    try:
        data = request.get_json()
        logger.info(f"Received Messenger message: {data}")
        response = messenger_handler.handle_message(data)
        return jsonify(response), 200
    except Exception as e:
        logger.error(f"Error handling Messenger message: {str(e)}")
        return jsonify({'error': str(e)}), 500

# API Routes for chat history
@app.route('/api/chat-history/<user_id>/<platform>', methods=['GET'])
def get_chat_history(user_id, platform):
    """Get chat history for a user"""
    try:
        limit = request.args.get('limit', 10, type=int)
        history = ai_agent.get_user_history(user_id, platform, limit)
        return jsonify({
            'status': 'success',
            'user_id': user_id,
            'platform': platform,
            'messages': history
        }), 200
    except Exception as e:
        logger.error(f"Error fetching chat history: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])
