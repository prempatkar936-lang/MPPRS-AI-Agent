import logging
import requests
from config import Config

logger = logging.getLogger(__name__)

class WhatsAppHandler:
    """Handler for WhatsApp messages"""
    
    def __init__(self, ai_agent):
        self.ai_agent = ai_agent
        self.api_token = Config.WHATSAPP_API_TOKEN
        self.phone_number_id = Config.WHATSAPP_PHONE_NUMBER_ID
        self.api_url = f"https://graph.instagram.com/v18.0/{self.phone_number_id}"
    
    def verify_webhook(self, request):
        """Verify WhatsApp webhook"""
        verify_token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        if verify_token == Config.FACEBOOK_VERIFY_TOKEN:
            return challenge
        return 'Invalid verify token', 403
    
    def handle_message(self, data):
        """Handle incoming WhatsApp message"""
        try:
            entry = data['entry'][0]
            changes = entry['changes'][0]
            message_data = changes['value']
            
            if 'messages' not in message_data:
                return {'status': 'success'}
            
            message = message_data['messages'][0]
            sender_phone = message['from']
            message_text = message['text']['body']
            
            # Generate AI reply
            reply = self.ai_agent.generate_reply(message_text, sender_phone, 'whatsapp')
            
            # Send reply
            self.send_message(sender_phone, reply)
            
            return {'status': 'success', 'message': 'Reply sent'}
        
        except Exception as e:
            logger.error(f"Error handling WhatsApp message: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def send_message(self, phone, message_text):
        """Send WhatsApp message"""
        try:
            headers = {'Authorization': f'Bearer {self.api_token}'}
            payload = {
                'messaging_product': 'whatsapp',
                'to': phone,
                'type': 'text',
                'text': {'body': message_text}
            }
            
            response = requests.post(f"{self.api_url}/messages", json=payload, headers=headers)
            logger.info(f"WhatsApp message sent to {phone}")
            return response.json()
        except Exception as e:
            logger.error(f"Error sending WhatsApp message: {str(e)}")

class InstagramHandler:
    """Handler for Instagram messages"""
    
    def __init__(self, ai_agent):
        self.ai_agent = ai_agent
        self.access_token = Config.INSTAGRAM_ACCESS_TOKEN
        self.business_account_id = Config.INSTAGRAM_BUSINESS_ACCOUNT_ID
    
    def verify_webhook(self, request):
        """Verify Instagram webhook"""
        verify_token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        if verify_token == Config.FACEBOOK_VERIFY_TOKEN:
            return challenge
        return 'Invalid verify token', 403
    
    def handle_message(self, data):
        """Handle incoming Instagram message"""
        try:
            entry = data['entry'][0]
            messaging = entry['messaging'][0]
            sender_id = messaging['sender']['id']
            message_text = messaging['message']['text']
            
            # Generate AI reply
            reply = self.ai_agent.generate_reply(message_text, sender_id, 'instagram')
            
            # Send reply
            self.send_message(sender_id, reply)
            
            return {'status': 'success', 'message': 'Reply sent'}
        
        except Exception as e:
            logger.error(f"Error handling Instagram message: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def send_message(self, sender_id, message_text):
        """Send Instagram message"""
        try:
            url = f"https://graph.instagram.com/v18.0/{sender_id}/messages"
            headers = {'Authorization': f'Bearer {self.access_token}'}
            payload = {'message': message_text}
            
            response = requests.post(url, json=payload, headers=headers)
            logger.info(f"Instagram message sent to {sender_id}")
            return response.json()
        except Exception as e:
            logger.error(f"Error sending Instagram message: {str(e)}")

class MessengerHandler:
    """Handler for Facebook Messenger messages"""
    
    def __init__(self, ai_agent):
        self.ai_agent = ai_agent
        self.page_access_token = Config.FACEBOOK_PAGE_ACCESS_TOKEN
    
    def verify_webhook(self, request):
        """Verify Messenger webhook"""
        verify_token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        if verify_token == Config.FACEBOOK_VERIFY_TOKEN:
            return challenge
        return 'Invalid verify token', 403
    
    def handle_message(self, data):
        """Handle incoming Messenger message"""
        try:
            entry = data['entry'][0]
            messaging = entry['messaging'][0]
            sender_id = messaging['sender']['id']
            
            if 'message' not in messaging:
                return {'status': 'success'}
            
            message_text = messaging['message'].get('text', '')
            
            if not message_text:
                return {'status': 'success'}
            
            # Generate AI reply
            reply = self.ai_agent.generate_reply(message_text, sender_id, 'messenger')
            
            # Send reply
            self.send_message(sender_id, reply)
            
            return {'status': 'success', 'message': 'Reply sent'}
        
        except Exception as e:
            logger.error(f"Error handling Messenger message: {str(e)}")
            return {'status': 'error', 'message': str(e)}
    
    def send_message(self, sender_id, message_text):
        """Send Messenger message"""
        try:
            url = f"https://graph.facebook.com/v18.0/me/messages"
            headers = {'Authorization': f'Bearer {self.page_access_token}'}
            payload = {
                'recipient': {'id': sender_id},
                'message': {'text': message_text}
            }
            
            response = requests.post(url, json=payload, headers=headers)
            logger.info(f"Messenger message sent to {sender_id}")
            return response.json()
        except Exception as e:
            logger.error(f"Error sending Messenger message: {str(e)}")
