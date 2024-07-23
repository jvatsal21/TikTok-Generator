FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libatspi2.0-0 \
    libxcomposite1 \
    libxdamage1 \
    wget \
    fontconfig

# Install the Komika Axis font
RUN mkdir -p /usr/share/fonts/truetype/
COPY ./fonts/KOMIKAX_.ttf /usr/share/fonts/truetype/

# Install Playwright browser binaries
RUN python3 -m playwright install chromium

# Run app.py when the container launches
ENTRYPOINT ["python", "main.py"]
