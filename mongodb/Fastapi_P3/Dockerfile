FROM ubuntu:20.04

ADD requirements.txt main.py pymongos.py DatafinitiElectronicsProductsPricingData.csv initiate.sh  ./

RUN apt update && apt install python3-pip libmysqlclient-dev -y && pip install -r requirements.txt

EXPOSE 8000

RUN ["chmod", "+x", "./initiate.sh"]
CMD ./initiate.sh