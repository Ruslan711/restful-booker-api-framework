FROM python:3.12-slim
WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends default-jre-headless curl \
    && curl -fsSL -o /tmp/allure.tgz https://github.com/allure-framework/allure2/releases/download/2.32.0/allure-2.32.0.tgz \
    && tar -xzf /tmp/allure.tgz -C /opt \
    && ln -s /opt/allure-2.32.0/bin/allure /usr/local/bin/allure \
    && rm /tmp/allure.tgz \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN chmod +x docker-entrypoint.sh
CMD ["./docker-entrypoint.sh"]
