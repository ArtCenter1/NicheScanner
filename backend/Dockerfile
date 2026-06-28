FROM python:3.11

WORKDIR /app

# Install WeasyPrint dependencies
# https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpango-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libcairo2 \
    xvfb

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8011

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8011"]