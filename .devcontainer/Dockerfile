FROM python:3.10

ENV WORKDIR workspace
WORKDIR /${WORKDIR}

ENV TZ Asia/Tokyo

RUN apt update \
 && apt upgrade -y

COPY requirements.txt /${WORKDIR}
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt



# >>> Development environment only
RUN apt install -y sudo

ARG USERNAME=user
ARG GROUPNAME=user
ARG UID=1000
ARG GID=1000
ARG PASSWORD=user

RUN groupadd -g ${GID} ${USERNAME} \
 && useradd -m -s /bin/bash -u ${UID} -g ${GROUPNAME} ${USERNAME} \
 && echo ${USERNAME}:${PASSWORD} | chpasswd \
 && echo "$USERNAME   ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
RUN chown -R ${USERNAME}:${GROUPNAME} /${WORKDIR}

USER ${USERNAME}

# <<<


RUN mkdir -p slackbot/log

# COPY slackbot /${WORKDIR}/slackbot

# CMD ["python3", "-m", "slackbot"]
