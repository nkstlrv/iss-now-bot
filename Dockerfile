FROM python:3.11-alpine
COPY . .
RUN pip3 install -r requirements.txt
CMD python main.py


