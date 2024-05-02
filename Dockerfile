FROM python:3.6-slim-buster

WORKDIR /app

COPY info.txt ./

RUN pip install -r info.txt

 COPY . . 

 EXPOSE 4000

 CMD ["flash", "run", "--host=0.0.0.0", "--port=4000"]