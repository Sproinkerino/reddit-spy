# Deployment Guide for Render

This guide explains how to deploy the Reddit Stalker API to Render using a Makefile for easy deployment.

## Prerequisites

- Render account (free tier available)
- GitHub repository with your code
- Reddit API credentials
- OpenAI API key

## 1. Prepare Your Repository

### File Structure
Make sure your repository has this structure:
```
reddit-stalk/
├── main.py                 # FastAPI application
├── requirements.txt        # Python dependencies
├── Makefile               # Deployment commands
├── .env.example           # Environment variables template
├── .gitignore            # Git ignore rules
├── README.md             # Main documentation
├── FRONTEND_API_GUIDE.md # Frontend integration guide
├── DEPLOYMENT_GUIDE.md   # This file
└── tests/                # Test files
    ├── test_api_simple.py
    └── run_tests.py
```

## 2. Create Makefile

Create a `Makefile` in your project root:

```makefile
# Makefile for Reddit Stalker API Deployment

.PHONY: help install test run deploy clean

# Default target
help:
	@echo "Available commands:"
	@echo "  install    - Install dependencies"
	@echo "  test       - Run tests"
	@echo "  run        - Run the application locally"
	@echo "  deploy     - Deploy to Render (manual trigger)"
	@echo "  clean      - Clean up temporary files"

# Install dependencies
install:
	pip install -r requirements.txt

# Run tests
test:
	python tests/test_api_simple.py

# Run the application locally
run:
	python main.py

# Deploy to Render (this is just a placeholder - actual deployment is via Render dashboard)
deploy:
	@echo "Deployment to Render is handled through the Render dashboard"
	@echo "Make sure your environment variables are set in Render"
	@echo "Trigger a manual deployment from the Render dashboard"

# Clean up temporary files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/

# Development setup
dev-setup: install
	@echo "Setting up development environment..."
	@if [ ! -f .env ]; then cp .env.example .env; echo "Created .env file from template"; fi
	@echo "Please edit .env file with your API credentials"

# Production check
prod-check:
	@echo "Checking production readiness..."
	@python -c "import main; print('✓ Main module imports successfully')"
	@python -c "import requests; print('✓ Requests module available')"
	@python -c "import praw; print('✓ PRAW module available')"
	@echo "✓ All checks passed"
```

## 3. Deploy to Render

### Step 1: Connect Repository
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Select your `reddit-stalk` repository

### Step 2: Configure Service
Use these settings:

**Basic Settings:**
- **Name**: `reddit-stalker-api`
- **Environment**: `Python 3`
- **Region**: Choose closest to your users
- **Branch**: `main` (or your default branch)

**Build & Deploy:**
- **Build Command**: `make install`
- **Start Command**: `python main.py`
- **Python Version**: `3.11` (or latest available)

### Step 3: Environment Variables
Add these environment variables in Render dashboard:

```
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=RedditStalker:v1.0.0 (by /u/yourusername)
OPENAI_API_KEY=sk-your_openai_api_key
```

**Important**: Never commit these values to your repository!

### Step 4: Advanced Settings
- **Auto-Deploy**: Enable for automatic deployments on git push
- **Health Check Path**: `/` (your health check endpoint)
- **Instance Type**: Free tier is sufficient for testing

## 4. Deployment Commands

### Local Development
```bash
# Install dependencies
make install

# Run tests
make test

# Run locally
make run

# Setup development environment
make dev-setup
```

### Production Deployment
```bash
# Check if everything is ready for production
make prod-check

# Clean up before deployment
make clean

# Deploy (triggers via Render dashboard)
make deploy
```

## 5. Post-Deployment

### Verify Deployment
1. Check the Render logs for any errors
2. Visit your deployed URL: `https://your-app.onrender.com`
3. Test the health endpoint: `https://your-app.onrender.com/`
4. Test the API docs: `https://your-app.onrender.com/docs`

### Update Frontend Configuration
Update your React app's API URL:
```javascript
const API_BASE_URL = 'https://your-app.onrender.com';
```

## 6. Monitoring and Maintenance

### Render Dashboard
- Monitor logs in real-time
- Check service health
- View deployment history
- Monitor resource usage

### Health Monitoring
The API includes a health check endpoint at `/` that returns:
```json
{
  "message": "Reddit Stalker API is running",
  "status": "healthy"
}
```

### Log Monitoring
Check Render logs for:
- API request/response logs
- Error messages
- Performance metrics

## 7. Troubleshooting

### Common Issues

#### Build Failures
```bash
# Check if all dependencies are in requirements.txt
pip freeze > requirements.txt

# Test locally first
make test
```

#### Environment Variable Issues
- Double-check all environment variables are set in Render
- Ensure no extra spaces or quotes in values
- Verify API keys are valid

#### Memory Issues
- Free tier has limited memory
- Consider upgrading if you hit limits
- Optimize your code for memory usage

#### Timeout Issues
- Render free tier has request timeouts
- Consider upgrading for longer requests
- Implement request queuing if needed

### Debug Commands
```bash
# Check Python version
python --version

# Check installed packages
pip list

# Test imports
python -c "import main; print('Success')"

# Check environment variables (locally)
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('REDDIT_CLIENT_ID:', bool(os.getenv('REDDIT_CLIENT_ID')))"
```

## 8. Scaling Considerations

### Free Tier Limitations
- 750 hours/month
- 512MB RAM
- Request timeouts
- No custom domains

### Upgrade Options
- **Starter Plan**: $7/month
  - Always-on
  - 512MB RAM
  - Custom domains
  - Better performance

- **Standard Plan**: $25/month
  - 1GB RAM
  - Better performance
  - Priority support

## 9. Security Best Practices

### Environment Variables
- Never commit `.env` files
- Use Render's environment variable system
- Rotate API keys regularly

### API Security
- Consider adding rate limiting
- Implement request validation
- Monitor for abuse

### CORS Configuration
If needed, add CORS middleware to your FastAPI app:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 10. Backup and Recovery

### Code Backup
- Your code is already backed up in GitHub
- Use Git tags for releases
- Keep deployment history in Render

### Data Backup
- This API is stateless (no database)
- All data comes from external APIs
- No backup needed for application data

## Support

- **Render Documentation**: https://render.com/docs
- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **GitHub Issues**: Create issues in your repository

## Cost Estimation

### Free Tier
- $0/month
- 750 hours (enough for light usage)
- Good for development and testing

### Paid Plans
- **Starter**: $7/month for always-on service
- **Standard**: $25/month for production use

Choose based on your usage patterns and requirements.
