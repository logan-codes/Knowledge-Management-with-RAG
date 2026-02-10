FROM python:3.11-slim

# Environment settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV HOME=/home/user
ENV PATH=/home/user/.local/bin:$PATH

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libxcb1 \
    tesseract-ocr \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Create a non-privileged user for HF Spaces
RUN useradd -m -u 1000 user
USER user

# Install Python dependencies
# Copy root requirements and remove Windows-specific packages
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy application code
COPY --chown=user . .

# Ensure start script is executable
RUN chmod +x start.sh

# HF Spaces default port is 7860 (will be used by Streamlit)
# FastAPI will run on 8000 internally
EXPOSE 7860

# Run the startup script
CMD ["./start.sh"]
