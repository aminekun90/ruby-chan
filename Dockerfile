FROM python:latest
LABEL Maintainer="aminekun90"
WORKDIR /ruby-chan
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD ["./run.sh"]