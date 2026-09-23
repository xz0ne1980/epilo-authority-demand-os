FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY bundle /tmp/bundle
COPY scripts/patch_navigation.py /tmp/patch_navigation.py

RUN cat \
    /tmp/bundle/exact_00000_10000.b64 \
    /tmp/bundle/exact_10000_20023.b64 \
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
    && python /tmp/patch_navigation.py \
    && python -c "from pathlib import Path; import re; p=Path('/app/static/app.js'); s=p.read_text(); s=re.sub(r'\\btop\\(', 'pageTop(', s); p.write_text(s)" \
    && rm -rf /tmp/bundle /tmp/essential.b64 /tmp/essential.zip

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["sh","-c","python -m uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
