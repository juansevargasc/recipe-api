# Alpine is a lightweight Linux distribution
FROM python:3.9-alpine3.13 

LABEL maintainer="Juanse"

# Recommended when running python in a contaner. Tells python not to buffer the standard output streams.
ENV PYTHONUNBUFFERED 1 

COPY ./requirements.txt /tmp/requirements.txt

COPY ./requirements.dev.txt /tmp/requirements.dev.txt

COPY ./app /app

# The default directory where any command will be executed
WORKDIR /app

EXPOSE 8000

ARG DEV=false

# Running the command concatenating using "&& \" allows to execute one single command instead of making many RUN statements.
# Is possible to use a venv in a container, it may be conflicts between the python version and the system version.
# tmp is removed after the installation of the requirements.
# At the end a new user is created, to avoid using the root user.
## "apk add --update --no-cache postgresql-client" installs the postgresql client in order for pyscopg2 to work. Note that since we're not using binary option, we will need to have the postgresql-dev package installed and it is not installed using pip, but with apk.
## "apk add --update --no-cache --virtual .tmp-build-deps" groups the packages that are going to be removed at the end of the installation with name .tmp-build-deps.
## "build-base postgresql-dev musl-dev" are packages under the name .tmp-build-deps needed to install psycopg2.
RUN python -m venv /py && \ 
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \    
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# The path is added to the environment variable PATH. 
# This is done to avoid using the full path to execute the python command.
ENV PATH="/py/bin:$PATH"

# The user is changed to the new user created.
USER django-user