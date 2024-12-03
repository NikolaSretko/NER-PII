# Nutze ein leichtgewichtiges Python-Basisimage
FROM python:3.10-slim

# Arbeitsverzeichnis
WORKDIR /app

# Kopiere requirements und installiere Abhängigkeiten
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den restlichen Code ins Image
COPY . .

# Setze die Umgebungsvariable für Flask
ENV FLASK_APP=app.py

# Exponiere Port 5000
EXPOSE 5000

# Starte die App
CMD ["python", "app.py"]