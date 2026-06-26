FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV LANGUAGE=C.UTF-8

COPY requirements.txt .

RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

COPY . .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONIOENCODING=utf-8

ENV BASE_URL=http://ruoyi-ui:80
ENV API_BASE_URL=http://ruoyi-admin:8080
ENV DB_HOST=mysql
ENV DB_PORT=3306
ENV DB_NAME=${DB_NAME:-ry-vue}
ENV DB_USERNAME=${DB_USERNAME:-root}
ENV DB_PASSWORD=${DB_PASSWORD:-123456}
ENV BROWSER=chromium
ENV HEADLESS=true
ENV TEST_USERNAME=${TEST_USERNAME:-admin}
ENV TEST_PASSWORD=${TEST_PASSWORD:-admin123}

CMD ["tail", "-f", "/dev/null"]
