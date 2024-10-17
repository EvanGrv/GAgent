FROM python:3.12.0

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["streamlit", "run", "Accueil.py"]
