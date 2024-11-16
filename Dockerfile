FROM python:3.9-slim

WORKDIR /app

# install OpenCV dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY utils/ utils/
COPY models/ models/

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0", "--server.port", "8501"]  