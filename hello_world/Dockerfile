FROM public.ecr.aws/lambda/python:3.11

WORKDIR ${LAMBDA_TASK_ROOT}

# Copy FFmpeg
COPY ffmpeg/ /usr/local/bin/

RUN yum install libsndfile -y

# install dependencies
COPY requirements.txt  ${LAMBDA_TASK_ROOT}
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# change permissions
RUN chmod +777 -R /usr/local/bin

# Copy function code
COPY app.py ${LAMBDA_TASK_ROOT}
COPY spectrogram_generation_functions.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.lambda_handler" ]