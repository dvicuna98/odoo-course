FROM python:3.10-bullseye as dependency-base

RUN apt-get update && \
    apt-get install -y  --no-install-recommends libsasl2-dev python-dev-is-python3 libldap2-dev libssl-dev

RUN mkdir -p /app

WORKDIR /app

COPY . .

RUN pip3 install -r ./requirements.txt

EXPOSE 8069

FROM dependency-base as production

CMD ["python3", "odoo-bin", "--addons-path=addons", "-c", "debian/odoo.conf"]


