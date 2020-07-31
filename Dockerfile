FROM python:3.8
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Set work directory
WORKDIR /code
# Install dependencies
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install pipenv==2018.11.26
RUN pip install uwsgi
COPY Pipfile Pipfile.lock /code/
RUN pipenv install --deploy --system
# Copy project
COPY . /code/