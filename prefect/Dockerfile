FROM prefecthq/prefect:2.7.7-python3.9

COPY requirements.txt .

RUN pip install -r requirements.txt --trusted-host pypi.python.org --no-cache-dir

COPY ./.kaggle/kaggle.json /root/.kaggle/kaggle.json

COPY /flows /opt/prefect/flows

RUN mkdir -p /opt/data