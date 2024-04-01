FROM python:3.11

WORKDIR /tests

# Copy FFmpeg
COPY ffmpeg/ /usr/local/bin/

# install dependencies
COPY requirements.txt  ./
RUN  pip3 install -r requirements.txt

# Copy function code
COPY app.py ./
COPY spectrogram_generation_functions.py ./
COPY mp3_b64.txt ./

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "python3", "./app.py" ]