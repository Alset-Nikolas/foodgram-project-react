FROM python:3.7-slim

COPY . .

RUN python -m pip install --upgrade pip 
RUN pip3 install -r requirements.txt --no-cache-dir
WORKDIR /foodgram_app



# CMD ["python3", "manage.py", "runserver"]
CMD ["gunicorn", "--bind", ":8000", "foodgram_app.wsgi:application", "--log-level", "debug"]