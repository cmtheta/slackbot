FROM python:3.10

ENV WORKDIR workspace
WORKDIR /${WORKDIR}

ENV TZ Asia/Tokyo

RUN apt update \
 && apt upgrade -y

COPY requirements.txt /${WORKDIR}
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir log

COPY slackbot /${WORKDIR}/slackbot

CMD ["python3", "-m", "slackbot"]
