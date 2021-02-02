FROM python:3
RUN mkdir /app
WORKDIR /app
COPY ./requirements.txt /app/.
RUN pip install \
    --no-cache-dir \
    --user \
    --no-warn-script-location \
    -r /app/requirements.txt \
    && rm /app/requirements.txt
COPY ./app /app
CMD python main.py

