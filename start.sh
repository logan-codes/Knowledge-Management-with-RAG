#!/bin/bash

# Start FastAPI server in the background
echo "Starting FastAPI server..."
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# Start Streamlit UI
echo "Starting Streamlit UI..."
streamlit run ui/Home.py --server.port 7860 --server.address 0.0.0.0
