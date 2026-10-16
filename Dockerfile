FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOST=0.0.0.0 \
    PORT=8001

# opencv-python (bắt buộc bởi insightface) cần libGL và glib trên Linux
RUN apt-get update \
    && apt-get install -y --no-install-recommends libgl1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY models/buffalo_l/ models/buffalo_l/
RUN test -f models/buffalo_l/det_10g.onnx && test -f models/buffalo_l/w600k_r50.onnx \
    || (echo "Thieu model trong models/buffalo_l (det_10g.onnx, w600k_r50.onnx)" && exit 1)

COPY run_server.py .
COPY src/ src/

RUN useradd --create-home appuser
USER appuser

EXPOSE 8001

HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
    CMD python -c "import os, urllib.request; urllib.request.urlopen('http://127.0.0.1:' + os.environ.get('PORT', '8001') + '/health', timeout=4)" || exit 1

CMD ["python", "run_server.py"]
