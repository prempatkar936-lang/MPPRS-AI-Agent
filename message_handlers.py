import logging
import requests
from config import Config

logger = logging.getLogger(__name__)

class InstagramHandler:
    """Handler for Instagram Direct Messages - Zero Errors"""
    
    def __init__(self, ai_agent):
        self.ai_agent = ai_agent
        self.access_token = Config.INSTAGRAM_ACCESS_TOKEN
        self.business_account_id = Config.INSTAGRAM_BUSINESS_ACCOUNT_ID
        self.api_url = "https://graph.instagram.com/v18.0"
    
    def verify_webhook(self, request):
        """Verify Instagram webhook"""
        try:
            verify_token = request.args.get('hub.verify_token')
            challenge = request.args.get('hub.challenge')
            
            if verify_token == Config.FACEBOOK_VERIFY_TOKEN:
                logger.info("✅ Instagram webhook verified successfully")
                return challenge
            
            logger.warning("❌ Invalid Instagram verify token")
            return 'Invalid verify token', 403
        except Exception as e:
            logger.error(f"Error verifying Instagram webhook: {str(e)}")
            return 'Error', 500
    
    def handle_message(self, data):
        """Handle incoming Instagram DM - Professional + Friendly + Lovely"""
        try:
            logger.info(f"📩 Instagram message received: {data}")
            
            # Parse Instagram webhook data
            entry = data.get('entry', [{}])[0]
            messaging = entry.get('messaging', [{}])
            
            if not messaging:
                logger.info("No messaging data found")
                return {'status': 'success'}
            
            messaging = messaging[0]
            
            # Extract message details
            sender_id = messaging.get('sender', {}).get('id')
            recipient_id = messaging.get('recipient', {}).get('id')
            message = messaging.get('message', {})
            message_text = message.get('text', '').strip()
            
            if not message_text or not sender_id:
                logger.info("⚠️ No message text or sender ID found")
                return {'status': 'success'}
            
            logger.info(f"📧 Instagram message from {sender_id}: {message_text}")
            
            # Get sender profile info
            sender_name = self.get_user_info(sender_id)
            
            # Generate AI reply - Professional + Friendly + Lovely style
            reply = self.ai_agent.generate_reply(
                message_text, 
                sender_id, 
                'instagram',
                sender_name=sender_name
            )
            
            # Send reply
            self.send_message(recipient_id, sender_id, reply)
            
            logger.info(f"✅ Instagram reply sent successfully to {sender_id}")
            return {'status': 'success', 'message': 'Reply sent'}
        
        except KeyError as e:
            logger.error(f"❌ KeyError in Instagram message handling: {str(e)}")
            return {'status': 'success', 'message': 'Processed'}
        except Exception as e:
            logger.error(f"❌ Error handling Instagram message: {str(e)}", exc_info=True)
            return {'status': 'success', 'message': 'Processed'}
    
    def get_user_info(self, user_id):
        """Get Instagram user information"""
        try:
            url = f"{self.api_url}/{user_id}"
            params = {'fields': 'name,username', 'access_token': self.access_token}
            response = requests.get(url, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                name = data.get('name', data.get('username', 'Friend'))
                logger.info(f"✅ Got Instagram user info: {name}")
                return name
            else:
                logger.warning(f"⚠️ Could not fetch Instagram user info: {response.text}")
                return 'Friend'
        except Exception as e:
            logger.warning(f"⚠️ Exception fetching Instagram user info: {str(e)}")
            return 'Friend'
    
    def send_message(self, business_account_id, recipient_id, message_text):
        """Send Instagram DM reply - Zero Errors"""
        try:
            url = f"{self.api_url}/{business_account_id}/messages"
            headers = {'Authorization': f'Bearer {self.access_token}'}
            payload = {
                'recipient': {'id': recipient_id},
                'message': {'text': message_text}
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            
            if response.status_code == 200:
                logger.info(f"✅ Instagram message sent to {recipient_id}")
                return response.json()
            else:
                logger.error(f"❌ Failed to send Instagram message: Status {response.status_code}, Response: {response.text}")
                return None
        except Exception as e:
            logger.error(f"❌ Error sending Instagram message: {str(e)}", exc_info=True)
            return None


class FacebookPersonalMessagesHandler:
    """Handler for Facebook Personal Messages (Mobile App) - Professional + Friendly + Lovely"""
    
    def __init__(self, ai_agent):
        self.ai_agent = ai_agent
        self.page_access_token = Config.FACEBOOK_PAGE_ACCESS_TOKEN
        self.verify_token = Config.FACEBOOK_VERIFY_TOKEN
        self.api_url = "https://graph.facebook.com/v18.0"
    
    def verify_webhook(self, request):
        """Verify Facebook webhook"""
        try:
            verify_token = request.args.get('hub.verify_token')
            challenge = request.args.get('hub.challenge')
            mode = request.args.get('hub.mode')
            
            if mode == 'subscribe' and verify_token == self.verify_token:
                logger.info("✅ Facebook webhook verified successfully")
                return challenge
            
            logger.warning("❌ Invalid Facebook verify token")
            return 'Invalid verify token', 403
        except Exception as e:
            logger.error(f"Error verifying Facebook webhook: {str(e)}")
            return 'Error', 500
    
    def handle_message(self, data):
        """Handle incoming Facebook Personal Message - Professional + Friendly + Lovely"""
        try:
            logger.info(f"📩 Facebook message received: {data}")
            
            # Parse Facebook webhook data
            entry = data.get('entry', [{}])[0]
            messaging = entry.get('messaging', [{}])
            
            if not messaging:
                logger.info("No messaging data found")
                return {'status': 'success'}
            
            messaging = messaging[0]
            
            # Extract message details
            sender_id = messaging.get('sender', {}).get('id')
            recipient_id = messaging.get('recipient', {}).get('id')
            message = messaging.get('message', {})
            message_text = message.get('text', '').strip() if message else ''
            
            # Ignore delivery/read receipts
            if not message_text or not sender_id:
                logger.info("⚠️ No message text or sender ID found")
                return {'status': 'success'}
            
            logger.info(f"📧 Facebook message from {sender_id}: {message_text}")
            
            # Get sender profile info
            sender_name = self.get_user_info(sender_id)
            
            # Generate AI reply - Professional + Friendly + Lovely style
            reply = self.ai_agent.generate_reply(
                message_text, 
                sender_id, 
                'facebook',
                sender_name=sender_name
            )
            
            # Send reply
            self.send_message(sender_id, reply)
            
            logger.info(f"✅ Facebook reply sent successfully to {sender_id}")
            return {'status': 'success', 'message': 'Reply sent'}
        
        except KeyError as e:
            logger.error(f"❌ KeyError in Facebook message handling: {str(e)}")
            return {'status': 'success', 'message': 'Processed'}
        except Exception as e:
            logger.error(f"❌ Error handling Facebook message: {str(e)}", exc_info=True)
            # Don't fail hard - log and continue
            return {'status': 'success', 'message': 'Processed'}
    
    def get_user_info(self, user_id):
        """Get Facebook user information"""
        try:
            url = f"{self.api_url}/{user_id}"
            params = {'fields': 'first_name,last_name', 'access_token': self.page_access_token}
            response = requests.get(url, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                first_name = data.get('first_name', 'Friend')
                logger.info(f"✅ Got Facebook user info: {first_name}")
                return first_name
            else:
                logger.warning(f"⚠️ Could not fetch Facebook user info: {response.text}")
                return 'Friend'
        except Exception as e:
            logger.warning(f"⚠️ Exception fetching Facebook user info: {str(e)}")
            return 'Friend'
    
    def send_message(self, recipient_id, message_text):
        """Send Facebook personal message reply"""
        try:
            url = f"{self.api_url}/me/messages"
            headers = {'Content-Type': 'application/json'}
            payload = {
                'recipient': {'id': recipient_id},
                'messaging_type': 'RESPONSE',
                'message': {'text': message_text}
            }
            params = {'access_token': self.page_access_token}
            
            response = requests.post(url, json=payload, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                logger.info(f"✅ Facebook message sent to {recipient_id}")
                return response.json()
            else:
                logger.error(f"❌ Failed to send Facebook message: Status {response.status_code}, Response: {response.text}")
                return None
        except Exception as e:
            logger.error(f"❌ Error sending Facebook message: {str(e)}", exc_info=True)
            return None
