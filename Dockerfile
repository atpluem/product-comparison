FROM python:3.9-slim
WORKDIR /prod-comp
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ src/
COPY main.py .
ENTRYPOINT ["python", "main.py"]

# Build
# docker build -t <tag name> .

# Run container
# docker run -v .:/prod-comp --rm <image name> --sku="TOYOTA-4RUNNER"