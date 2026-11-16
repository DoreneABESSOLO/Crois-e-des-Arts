FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONPATH=/app/src
# Utilisateur non root (moindre privilège)
RUN useradd -m poc && chown -R poc /app
USER poc
CMD ["sh", "-c", "python -m unittest discover -s tests -v && python -m fashmatch_poc.pipeline"]
