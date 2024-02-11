FROM python:3.8-slim as base

RUN apt-get update \
  && apt-get install -y --no-install-recommends python3-dev libpq-dev gcc curl g++ \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip

WORKDIR /opt/webapp
COPY Pipfile* /opt/webapp/

RUN pip3 install --no-cache-dir -q 'pipenv==2022.9.24'
RUN pipenv install --deploy --system --skip-lock


COPY . /opt/webapp

FROM base as release

ARG SECRET_KEY

COPY --from=base /root/.local /root/.local
COPY --from=base /opt/webapp/manage.py /opt/webapp/manage.py

WORKDIR /opt/webapp

# Add runtime user with respective access permissions
RUN groupadd -r django \
  && useradd -d /opt/webapp -r -g django django \
  && chown django:django -R /opt/webapp

USER django

ENV PATH=/root/.local/bin:$PATH

# Collect static files and serve app
RUN python3 manage.py collectstatic --no-input
CMD waitress-serve --port=$PORT cold_fusion_fishing.wsgi:application
