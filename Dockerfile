FROM python:latest
LABEL Maintainer="aminekun90"
WORKDIR /ruby-chan
ENV VIRTUAL_ENV "/opt/venv"
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
# Install dependencies:
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["./run.sh"]