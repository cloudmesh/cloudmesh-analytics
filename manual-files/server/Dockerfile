FROM continuumio/miniconda3
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN conda install --file requirements.txt
RUN pip install connexion[swagger-ui]
COPY . .
CMD [ "python", "./server.py" ]