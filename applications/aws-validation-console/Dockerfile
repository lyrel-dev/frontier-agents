FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 \
    CONSOLE_DATA=/data CONSOLE_CONFIG=/config/config.json CONSOLE_BIND=0.0.0.0 \
    AWS_EC2_METADATA_DISABLED=true
WORKDIR /opt/validation-console
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
 && groupadd --gid 10001 console \
 && useradd --uid 10001 --gid 10001 --home-dir /home/console --create-home console \
 && mkdir -p /data /config \
 && chown 10001:10001 /data
COPY app ./app
COPY run.py build_ui.py build_metrics.py ./
COPY static ./static
COPY examples ./examples
RUN python build_ui.py
COPY config.json /config/config.json
USER 10001:10001
EXPOSE 8787
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8787/healthz', timeout=3)"
CMD ["python", "run.py"]
