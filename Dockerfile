FROM python:3.11-slim

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    rm -f /etc/apt/apt.conf.d/docker-clean; \
    echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache \
    && apt update \
    && apt install -y --no-install-recommends build-essential libpq-dev locales tree --fix-missing \
    || (sleep 5 && apt install -y build-essential libpq-dev locales tree) \
    && sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen \
    && dpkg-reconfigure --frontend=noninteractive locales \
    && apt clean

WORKDIR /NIC_astrawood

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=ru_RU.UTF-8
ENV LC_ALL=ru_RU.UTF-8

COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# Automatically run collectstatic during build
RUN python manage.py collectstatic --noinput || echo "Collectstatic failed"

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]