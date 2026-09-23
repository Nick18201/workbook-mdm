# Dockerfile optimisé pour Google Cloud Run
FROM python:3.11-slim

# Empêche Python d'écrire des fichiers .pyc et assure le flush immédiat des logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080
ENV PYTHONPATH="/app:/app/Scripts"

WORKDIR /app

# Installation des dépendances système légères si nécessaire
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copie et installation des dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie des briques applicatives, polices et illustrations
COPY assets/ ./assets/
COPY Scripts/ ./Scripts/
COPY server/ ./server/

# Port d'écoute par défaut Cloud Run
EXPOSE 8080

# Lancement du serveur avec la variable dynamique $PORT fournie par Cloud Run
CMD uvicorn server.app:app --host 0.0.0.0 --port ${PORT:-8080}
