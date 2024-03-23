FROM python:3.11

RUN apt-get clean && apt-get update

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY acled.py .
COPY setup.py .

ENTRYPOINT [ "python", "setup.py" ]