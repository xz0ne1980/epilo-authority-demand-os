FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY bundle /tmp/bundle

RUN cat \
    /tmp/bundle/part00.b64 \
    /tmp/bundle/missing_20023_40000.b64 \
    /tmp/bundle/p1_00 \
    /tmp/bundle/p1_01 \
    /tmp/bundle/p1_02 \
    /tmp/bundle/p1_03 \
    /tmp/bundle/p2_00 \
    /tmp/bundle/p2_01 \
    /tmp/bundle/p2_02 \
    > /tmp/essential.b64 \
    && python -c "import base64,pathlib,zipfile; p=pathlib.Path('/tmp/essential.b64'); z=pathlib.Path('/tmp/essential.zip'); z.write_bytes(base64.b64decode(p.read_text())); zipfile.ZipFile(z).extractall('/app')" \
    && rm -rf /tmp/bundle /tmp/essential.b64 /tmp/essential.zip

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["sh","-c","python -m uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
