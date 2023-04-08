FROM prefecthq/prefect:2.7.7-python3.9

COPY requirements.txt .

RUN pip install -r requirements.txt --trusted-host pypi.python.org --no-cache-dir

RUN export KAGGLE_USERNAME="aliescont"
RUN export KAGGLE_KEY="c9449a0a0f3a4cbbf39f151def2c85b5"

RUN mkdir -p /opt/prefect/data/source
COPY flows /opt/prefect/flows
COPY data /opt/prefect/data