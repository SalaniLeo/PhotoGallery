FROM python:3.9.2-alpine

# Install dependencies required for creating a virtual environment
RUN apk add --no-cache \
    gcc \
    libffi-dev \
    musl-dev \
    openssl-dev \
    python3-dev

# upgrade pip
RUN pip install --upgrade pip

# get curl for healthchecks
RUN apk add curl

# permissions and nonroot user for tightened security
RUN adduser -D nonroot
RUN mkdir /home/app/ && chown -R nonroot:nonroot /home/app
RUN mkdir -p /var/log/flask-app && touch /var/log/flask-app/flask-app.err.log && touch /var/log/flask-app/flask-app.out.log
RUN chown -R nonroot:nonroot /var/log/flask-app
WORKDIR /home/app
USER nonroot

# copy all the files to the container
COPY --chown=nonroot:nonroot . .

# python setup and venv in one RUN command
ENV VIRTUAL_ENV=/home/app/venv
RUN python -m venv $VIRTUAL_ENV && \
    $VIRTUAL_ENV/bin/pip install --upgrade pip && \
    $VIRTUAL_ENV/bin/pip install -r requirements.txt

# set PATH for the virtual environment
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# define the port number the container should expose
EXPOSE 8080

CMD ["python", "app.py"]
