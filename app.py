from flask import Flask, request, jsonify
from flask_cors import CORS
from config import config
from database import init_db
from ai_agent import AIAgent
from message_handlers import InstagramHandler, FacebookPersonalMessagesHandler
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
    logger.info("✅ Database initialized successfully")
except Exception as e:
    logger.error(f"❌ Failed to initialize database: {str(e)}")

# Initialize handlers
try:
    ai_agent = AIAgent()
    instagram_handler = InstagramHandler(ai_agent)
    facebook_handler = FacebookPersonalMessagesHandler(ai_agent)
    logger.info("✅ All handlers initialized successfully")
except Exception as e:
    logger.error(f"❌ Failed to initialize handlers: {str(e)}")

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': '✅ healthy',
        'service': 'MPPRS AI Agent - Prem Patkar',
        'platforms': ['Instagram DMs', 'Facebook Personal Messages'],
        'style': 'Professional + Friendly + Lovely',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '2.0.0'
    }), 200

# ============================================================
# INSTAGRAM ROUTES
# ============================================================
@app.route('/webhook/instagram', methods=['GET'])
def instagram_verify():
    """Verify Instagram webhook"""
    logger.info("📱 Instagram webhook verification requested")
    return instagram_handler.verify_webhook(request)

@app.route('/webhook/instagram', methods=['POST'])
def instagram_webhook():
    """Handle Instagram Direct Messages"""
    try:
        data = request.get_json()
        logger.info(f"📩 Received Instagram message: {data}")
        response = instagram_handler.handle_message(data)
        return jsonify(response), 200
    except Exception as e:
        logger.error(f"❌ Error handling Instagram message: {str(e)}", exc_info=True)
        return jsonify({'status': 'success', 'message': 'Processed'}), 200

# ============================================================
# FACEBOOK PERSONAL MESSAGES ROUTES
# ============================================================
@app.route('/webhook/facebook', methods=['GET'])
def facebook_verify():
    """Verify Facebook webhook"""
    logger.info("📱 Facebook webhook verification requested")
    return facebook_handler.verify_webhook(request)

@app.route('/webhook/facebook', methods=['POST'])
def facebook_webhook():
    """Handle Facebook Personal Messages (Mobile App)"""
    try:
        data = request.get_json()
        logger.info(f"📩 Received Facebook message: {data}")
        response = facebook_handler.handle_message(data)
        return jsonify(response), 200
    except Exception as e:
        logger.error(f"❌ Error handling Facebook message: {str(e)}", exc_info=True)
        return jsonify({'status': 'success', 'message': 'Processed'}), 200

# ============================================================
# API ROUTES FOR CHAT HISTORY
# ============================================================
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
            'message_count': len(history),
            'messages': history
        }), 200
    except Exception as e:
        logger.error(f"❌ Error fetching chat history: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/api/status', methods=['GET'])
def api_status():
    """Get API status"""
    return jsonify({
        'status': '✅ Online',
        'service': 'MPPRS AI Agent',
        'owner': 'Prem Patkar',
        'platforms': ['Instagram', 'Facebook'],
        'ai_style': 'Professional + Friendly + Lovely',
        'timestamp': datetime.utcnow().isoformat()
    }), 200

# ============================================================
# ERROR HANDLERS
# ============================================================
@app.errorhandler(404)
def not_found(error):
    logger.warning(f"⚠️ 404 - Endpoint not found")
    return jsonify({'error': 'Endpoint not found', 'status': 404}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"❌ 500 - Internal server error: {str(error)}")
    return jsonify({'error': 'Internal server error', 'status': 500}), 500

@app.before_request
def log_request():
    """Log incoming requests"""
    logger.info(f"📨 {request.method} {request.path}")

@app.after_request
def log_response(response):
    """Log outgoing responses"""
    logger.info(f"📤 Response status: {response.status_code}")
    return response

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    debug_mode = app.config.get('DEBUG', False)
    
    logger.info(f"""
    ╔════════════════════════════════════════════════════════════╗
    ║        🚀 MPPRS AI AGENT - STARTING UP 🚀                  ║
    ║                                                              ║
    ║  Owner: Prem Patkar                                         ║
    ║  Platforms: Instagram DMs, Facebook Personal Messages       ║
    ║  Style: Professional + Friendly + Lovely                    ║
    ║  Port: {port}                                                 ║
    ║  Debug: {debug_mode}                                            ║
    ║  Version: 2.0.0                                             ║
    ║                                                              ║
    ║  Webhooks:                                                   ║
    ║  - Instagram: /webhook/instagram                            ║
    ║  - Facebook: /webhook/facebook                              ║
    ║                                                              ║
    ║  Health Check: GET /                                        ║
    ║  Status: GET /api/status                                    ║
    ║                                                              ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
