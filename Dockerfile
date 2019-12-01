FROM python:3.8.0-buster

COPY *.py requirements.txt /app/

RUN pip3 install -r /app/requirements.txt

# downloads nltk punkt recognizer
RUN python3 -m nltk.downloader punkt

WORKDIR /app

ENTRYPOINT ["python3", "whats_next.py"]