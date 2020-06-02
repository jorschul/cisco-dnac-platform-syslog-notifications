FROM python:3.8-slim
WORKDIR /cisco-dnac-platform-syslog-notifications/
COPY ./ ./
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "run.py"]
