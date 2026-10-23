FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 LAB_BIND=0.0.0.0 LAB_DATA=/data
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
 && groupadd --gid 10001 lab \
 && useradd --uid 10001 --gid 10001 --no-create-home lab \
 && mkdir /data && chown 10001:10001 /data && chmod 700 /data
COPY lab/ ./lab/
COPY static/ ./static/
COPY run.py worker.py configure.py acceptance.py config.json ./
USER 10001:10001
VOLUME ["/data"]
EXPOSE 8787
HEALTHCHECK --interval=30s --timeout=4s --retries=3 CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8787/readyz',timeout=3)"
CMD ["python","run.py","--with-worker"]
