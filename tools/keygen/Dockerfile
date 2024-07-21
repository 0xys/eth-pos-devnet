FROM python:alpine3.14 as builder
RUN apk add --update git bash gcc libc-dev linux-headers
WORKDIR /src

RUN bash -c "git clone https://github.com/ethereum/staking-deposit-cli.git"

WORKDIR /src/staking-deposit-cli
COPY main.py ./staking_deposit

RUN chmod +x setup.py
RUN chmod +x ./staking_deposit/main.py

RUN pip3 install -r requirements.txt
RUN python3 setup.py install

# Run my_script.py when the container launches
ENTRYPOINT ["python3", "./staking_deposit/main.py"]
