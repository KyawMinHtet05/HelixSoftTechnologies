FROM python:3.10

RUN apt-get update && apt-get install -y \
    python3-tk \
    tk \
    x11-apps \
    xauth \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

ENV DISPLAY=host.docker.internal:0

ENV XVFB_ARGS="-screen 0 1024x768x24"

WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install requests
COPY . .

RUN mkdir -p /root/ClinicalData/Downloads \
    /root/ClinicalData/Archive \
    /root/ClinicalData/Errors

CMD ["python", "HelixSoftTechnologies.py"]