# Gradient Copilot Backend

## 📋 Assignment Details
This project was built for **Gradient's Software Engineer Intern (Summer 2025)** take-home assignment - **Option 1: Copilot Learning Assistant Chatbot**.

## 🔗 Links
**Github**: https://github.com/vissutagunawan/gradient-copilot-be \
**Deployment URL**: https://gradient-copilot-be-production.up.railway.app \
**API Documentation**: https://gradient-copilot-be-production.up.railway.app/docs

## 🛠️ Tech Stack
- Framework: FastAPI (Python)
- AI/LLM: Google Gemini API (Gemini 1.5 Flash)
- Search: SerpAPI for educational content discovery
- Image Processing: Pillow (PIL)
- Deployment: Railway

## ✨ Features (Assignment Requirements Met)
- 🤖 Free LLM API integration (Google Gemini)
- 🔍 Real-time material search and recommendations.
- 📷 Image upload and analysis support
- 🚀 Deployed to free cloud service (Railway)

## 🚀 Feature Improvisation
**Beyond Assignment Requirements:**

Instead of using static dummy data, this application implements live **SerpAPI integration** for real-time web search functionality. The system intelligently searches for educational content from trusted sources (YouTube, Coursera, Khan Academy, etc.) and provides users with current, relevant learning materials. Dummy data serves as a reliable fallback mechanism when external APIs encounter errors.

## 🔮 Future Development
- Integrate with Gradient's study materials for a more specialized material recommendations.
- RAG Implementation using study material content database for better material retrieval mechanism and seamless integration with copilot.
- Docker containerization for deployment consistency and dependency isolation.
- Deploy to existing Kubernetes cluster as a service (Copilot service) for auto load balancing and auto scaling.