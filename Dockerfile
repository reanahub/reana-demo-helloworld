FROM python:2.7-alpine
ADD . /code
WORKDIR /code
CMD ["python", "helloworld.py", \
     "--name", "John Doe", \
     "--outputfile", "output/greetings.txt", \
     "--sleeptime", "1"]
