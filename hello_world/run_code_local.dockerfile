FROM python:3.11

WORKDIR /tests

# install dependencies
COPY requirements.txt  ./
RUN  pip3 install -r requirements.txt

# Copy function code
COPY app.py ./
COPY spectrogram_generation_functions.py ./

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "python3", "./app.py" ]