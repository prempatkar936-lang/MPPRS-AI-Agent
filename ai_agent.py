import openai
import logging
from config import Config
from database import SessionLocal, Message, User, Conversation
from datetime import datetime

logger = logging.getLogger(__name__)

class AIAgent:
    """AI Agent for processing and responding to messages - Professional + Friendly + Lovely Style"""
    
    def __init__(self):
        openai.api_key = Config.OPENAI_API_KEY
        self.model = Config.OPENAI_MODEL
        self.temperature = Config.OPENAI_TEMPERATURE
        self.max_tokens = Config.OPENAI_MAX_TOKENS
        self.db = SessionLocal()
    
    def get_conversation_context(self, user_id, platform, limit=5):
        """Get previous messages for context"""
        try:
            messages = self.db.query(Message).filter(
                Message.user_id == user_id,
                Message.platform == platform
            ).order_by(Message.timestamp.desc()).limit(limit).all()
            
            context = []
            for msg in reversed(messages):
                context.append(f"User: {msg.message_text}")
                if msg.reply_text:
                    context.append(f"Assistant: {msg.reply_text}")
            
            return "\n".join(context)
        except Exception as e:
            logger.error(f"Error getting conversation context: {str(e)}")
            return ""
    
    def generate_reply(self, user_message, user_id, platform, sender_name="Friend"):
        """Generate AI reply using OpenAI - Professional + Friendly + Lovely"""
        try:
            # Get conversation context
            context = self.get_conversation_context(user_id, platform)
            
            # Prem Patkar's personal style - Professional + Friendly + Lovely
            system_message = f"""You are Prem Patkar's personal AI assistant. You respond on behalf of Prem to messages on {platform}.

Your personality:
- Professional yet warm and approachable
- Friendly and engaging in conversations
- Lovely and caring - show genuine interest in people
- Casual and natural language (use Hindi-English mix when appropriate)
- Use emojis occasionally but not overdone
- Keep responses concise but meaningful (under 500 characters)
- Be helpful and honest
- Remember context from previous messages
- Make people feel valued and heard

When responding:
- Acknowledge what the person said
- Respond genuinely and authentically
- Use the person's name if you know it ({sender_name})
- Add warmth and personality
- Never sound robotic or generic
- Be yourself (Prem's personality)

Format: Keep it natural, conversational, and warm."""
            
            # Build conversation for OpenAI
            messages = [
                {"role": "system", "content": system_message},
            ]
            
            if context:
                messages.append({"role": "user", "content": f"Previous conversation context:\n{context}"})
            
            messages.append({"role": "user", "content": user_message})
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            reply = response.choices[0].message.content.strip()
            
            # Store message in database
            self.store_message(user_id, platform, user_message, reply)
            
            logger.info(f"✅ Generated reply for user {user_id} on {platform}")
            return reply
        
        except openai.error.RateLimitError:
            logger.error("⚠️ OpenAI rate limit exceeded")
            return "Thanks for reaching out! I'm a bit busy right now, but I'll get back to you soon! 😊"
        except openai.error.AuthenticationError:
            logger.error("❌ OpenAI authentication failed")
            return "Sorry, I'm having trouble responding right now. Please try again in a moment! 🙏"
        except Exception as e:
            logger.error(f"❌ Error generating reply: {str(e)}")
            return "Thanks for your message! I'll respond as soon as I can! 😊"
    
    def store_message(self, user_id, platform, message_text, reply_text):
        """Store message in database"""
        try:
            # Ensure user exists
            user = self.db.query(User).filter(
                User.user_id == user_id,
                User.platform == platform
            ).first()
            
            if not user:
                user = User(
                    user_id=user_id,
                    platform=platform,
                    name=user_id,
                    created_at=datetime.utcnow()
                )
                self.db.add(user)
                self.db.commit()
                logger.info(f"✅ Created new user: {user_id}")
            
            # Store message
            msg = Message(
                user_id=user_id,
                platform=platform,
                message_text=message_text,
                reply_text=reply_text,
                message_type='incoming',
                timestamp=datetime.utcnow(),
                processed=True
            )
            self.db.add(msg)
            
            # Update or create conversation
            conv = self.db.query(Conversation).filter(
                Conversation.user_id == user_id,
                Conversation.platform == platform,
                Conversation.is_active == True
            ).first()
            
            if not conv:
                conv = Conversation(
                    user_id=user_id,
                    platform=platform,
                    total_messages=0,
                    created_at=datetime.utcnow()
                )
                self.db.add(conv)
            
            conv.total_messages += 1
            conv.updated_at = datetime.utcnow()
            
            self.db.commit()
            logger.info(f"✅ Message stored for user {user_id}")
        
        except Exception as e:
            logger.error(f"❌ Error storing message: {str(e)}")
            self.db.rollback()
    
    def get_user_history(self, user_id, platform, limit=10):
        """Get user chat history"""
        try:
            messages = self.db.query(Message).filter(
                Message.user_id == user_id,
                Message.platform == platform
            ).order_by(Message.timestamp.desc()).limit(limit).all()
            
            return [{"user": msg.message_text, "ai": msg.reply_text, "timestamp": msg.timestamp.isoformat()} 
                    for msg in reversed(messages)]
        except Exception as e:
            logger.error(f"❌ Error fetching user history: {str(e)}")
            return []
    
    def close(self):
        """Close database connection"""
        self.db.close()
