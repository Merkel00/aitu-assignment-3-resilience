FROM python:3.12-slim
WORKDIR /app
COPY registration-demo-app.py /app/app.py
USER 65532:65532
EXPOSE 8080
CMD ["python", "-u", "/app/app.py"]
