FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /idealyard
WORKDIR /idealyard
COPY . /idealyard
RUN pip install -p Pipfile