# The main app
FROM python:3

WORKDIR /usr/app

COPY . .

# install requirements
RUN pip install --no-cache-dir -r requirements.txt

CMD python main.py