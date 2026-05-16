# MPPRS AI Agent 🤖

**MPPRS** - A powerful AI automation agent for WhatsApp, Instagram, and Facebook Messenger

## Overview

MPPRS AI Agent is a sophisticated chatbot solution that:
- 🚀 Automatically responds to messages on WhatsApp, Instagram, and Messenger
- 🧠 Uses OpenAI's GPT-3.5-turbo for intelligent, casual responses
- 💾 Stores conversation history in Cloud SQL (PostgreSQL)
- ☁️ Deploys on Google Cloud Run
- 🔐 Secure credential management with .env files
- 📱 Multi-platform support

## Features

✅ WhatsApp Integration
✅ Instagram Direct Messages
✅ Facebook Messenger
✅ OpenAI GPT Integration
✅ PostgreSQL Database (MPPRS)
✅ Google Cloud Run Deployment
✅ Conversation History & Context
✅ Casual, Friendly Responses
✅ Error Handling & Logging
✅ Production Ready

## Prerequisites

- Python 3.11+
- Google Cloud Account
- OpenAI API Key
- WhatsApp Business Account
- Instagram Business Account
- Facebook Business Account
- Docker
- Terraform (optional, for IaC)

## Setup Instructions

### 1. Clone Repository

```bash
git clone https://github.com/prempatkar936-lang/MPPRS-AI-Agent.git
cd MPPRS-AI-Agent
```

### 2. Environment Setup

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```bash
OPENAI_API_KEY=your_openai_api_key
GOOGLE_CLOUD_PROJECT_ID=your_project_id
DATABASE_USER=postgres
DATABASE_PASSWORD=your_secure_password
DATABASE_HOST=your_cloud_sql_ip
DATABASE_NAME=MPPRS
WHATSAPP_API_TOKEN=your_whatsapp_token
INSTAGRAM_ACCESS_TOKEN=your_instagram_token
FACEBOOK_PAGE_ACCESS_TOKEN=your_facebook_token
FACEBOOK_VERIFY_TOKEN=your_verify_token
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize Database

```bash
python -c "from database import init_db; init_db()"
```

### 5. Run Locally

```bash
python app.py
```

Server will start on `http://localhost:8080`

## Google Cloud Deployment

### Using Terraform

```bash
# Initialize Terraform
terraform init

# Create terraform.tfvars
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your values

# Plan deployment
terraform plan

# Apply deployment
terraform apply
```

### Using Cloud Build

```bash
# Deploy using Cloud Build
gcloud builds submit --config cloudbuild.yaml
```

### Manual Deployment

```bash
# Build Docker image
docker build -t mpprs-ai-agent .

# Push to Artifact Registry
docker tag mpprs-ai-agent gcr.io/YOUR_PROJECT_ID/mpprs-ai-agent
docker push gcr.io/YOUR_PROJECT_ID/mpprs-ai-agent

# Deploy to Cloud Run
gcloud run deploy mpprs-ai-agent \
  --image gcr.io/YOUR_PROJECT_ID/mpprs-ai-agent \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## API Endpoints

### Health Check
```
GET /
```

### WhatsApp Webhook
```
GET/POST /webhook/whatsapp
```

### Instagram Webhook
```
GET/POST /webhook/instagram
```

### Messenger Webhook
```
GET/POST /webhook/messenger
```

### Chat History
```
GET /api/chat-history/{user_id}/{platform}?limit=10
```

## Database Schema

### Users Table
- `id` (Primary Key)
- `user_id` (Unique, indexed)
- `platform` (whatsapp/instagram/messenger)
- `name`
- `phone` (nullable)
- `email` (nullable)
- `created_at`
- `updated_at`
- `is_active`

### Messages Table
- `id` (Primary Key)
- `user_id` (indexed)
- `platform`
- `message_text`
- `reply_text`
- `message_type`
- `timestamp`
- `processed`

### Conversations Table
- `id` (Primary Key)
- `user_id` (indexed)
- `platform`
- `conversation_summary`
- `total_messages`
- `created_at`
- `updated_at`
- `is_active`

## Configuration Details

### OpenAI Settings
- **Model**: gpt-3.5-turbo
- **Temperature**: 0.7 (for casual, creative responses)
- **Max Tokens**: 500 (concise replies)

### Cloud Run Settings
- **Region**: us-central1
- **Memory**: 512MB (configurable)
- **Timeout**: 3600s (1 hour)
- **Concurrency**: 80 (default)

## Webhook Setup

### WhatsApp
1. Go to Facebook Business Manager
2. Create WhatsApp Business Account
3. Configure webhook: `https://your-cloud-run-url/webhook/whatsapp`
4. Add verify token in `.env`

### Instagram
1. Create Instagram Business Account
2. Configure webhook: `https://your-cloud-run-url/webhook/instagram`
3. Subscribe to Instagram events

### Messenger
1. Create Facebook App
2. Create Page Access Token
3. Configure webhook: `https://your-cloud-run-url/webhook/messenger`
4. Subscribe to messaging events

## Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=.
```

## Troubleshooting

### Database Connection Issues
```bash
# Test Cloud SQL connection
gcloud sql connect mpprs-db-instance --user=postgres
```

### API Key Issues
- Verify `.env` file has correct keys
- Check API key permissions
- Ensure keys are not expired

### Webhook Verification Fails
- Verify token matches in app and provider
- Check HTTPS is being used
- Verify endpoint is accessible

## Logging

Logs are sent to Google Cloud Logging:

```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=mpprs-ai-agent" --limit 50 --format json
```

## Performance Optimization

- Database connection pooling enabled
- Message caching for quick responses
- Async message processing
- Database indexes on frequently queried fields

## Security Considerations

✅ API keys stored in .env (never in code)
✅ HTTPS only for webhooks
✅ Database password protection
✅ Input validation and sanitization
✅ Error messages don't expose sensitive info
✅ CORS properly configured

## Contributing

Contributions welcome! Please:
1. Fork repository
2. Create feature branch
3. Make changes
4. Submit pull request

## License

MIT License - see LICENSE file

## Support

For issues and questions:
- Open GitHub Issues
- Email: prempatkar936-lang@example.com

## Roadmap

- [ ] Telegram integration
- [ ] Multi-language support
- [ ] Advanced NLP features
- [ ] Custom training models
- [ ] Analytics dashboard
- [ ] Voice message support

---

**Made with ❤️ by MPPRS Team**
