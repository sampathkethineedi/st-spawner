FROM python:3.7

EXPOSE 7000

RUN pip install streamlit pydantic

COPY ./app /app
WORKDIR /app

CMD streamlit run spawner.py --server.port 7000 --server.baseUrlPath "/st-spawner" --browser.serverAddress "0.0.0.0"