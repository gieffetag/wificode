FROM python:3.8-slim as builder
RUN apt-get update \
	&& apt-get install gcc libev-dev git -y \
	&& apt-get clean

COPY ./requirements.txt /app/requirements.txt
WORKDIR app
RUN pip install \
    --no-cache-dir \
    --user \
    --no-warn-script-location \
    -r /app/requirements.txt \
    && rm /app/requirements.txt


FROM python:3.8-slim as app
RUN apt-get update \
	&& apt-get install libev-dev -y \
	&& apt-get clean

COPY --from=builder /root/.local /root/.local
COPY ./app /app
WORKDIR app
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "-u" ,"main.py"]



