FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install fastapi uvicorn groq python-dotenv
CMD ["python", "-m", "uvicorn", "api_agent:app", "--host", "0.0.0.0", "--port", "8000"]