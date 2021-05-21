from alpine:latest

ENV http_proxy http://wwwproxy.unimelb.edu.au:8000/
ENV https_proxy http://wwwproxy.unimelb.edu.au:8000/

RUN apk add cmd:pip3
RUN apk add --no-cache python3-dev \
    && pip install --upgrade pip 

WORKDIR /app

COPY . /app

RUN pip3 --no-cache-dir install -r requirements.txt

EXPOSE 6100

ENTRYPOINT ["python3"]
CMD ["server.py"]
