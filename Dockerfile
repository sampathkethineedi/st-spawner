FROM python:3.7

EXPOSE 7000

COPY ./app /app
WORKDIR /app

RUN pip install streamlit

CMD streamlit run spawner.py --server.port 7000