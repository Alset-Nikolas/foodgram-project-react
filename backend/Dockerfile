FROM python:3.7-slim

WORKDIR /backend_foodgram_app

COPY requirements.txt .

RUN python -m pip install --upgrade pip 
RUN pip3 install -r requirements.txt --no-cache-dir

COPY /foodgram_app ./foodgram_app
WORKDIR /backend_foodgram_app/foodgram_app



# CMD ["python3", "manage.py", "collectstatic"]
# CMD ["gunicorn", "--bind", ":8000", "foodgram_app.wsgi:application", "--log-level", "debug"]

ADD docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod a+x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]