print('Starting import...')
import json
import librosa
import numpy as np
import boto3
import os
from datetime import datetime
from tempfile import TemporaryDirectory
import base64
import uuid
from pathlib import Path
from typing import Dict
from spectrogram_generation_functions import multithreading_sampling


def invoke_second_lambda(function_name: str, payload: Dict, invocation_type='RequestResponse'):
    """
    Parameters:
        function_name [str]: the name of the second lambda to be invoked
        payload [dict[str, list[str]]: the payload to be sent
        invocation_type [str]: default RequestResponse. invocation type can be 'RequestResponse' or 'Event' (asynchronous)
    Returns:
        result: the return of the other lambda
    """
    # Initialize the Lambda client
    client = boto3.client('lambda')

    # Convert payload to JSON
    payload = json.dumps(payload)

    # Invoke the Lambda function
    response = client.invoke(
        FunctionName=function_name,
        InvocationType=invocation_type,
        Payload=payload
    )

    # Handle the response
    response_payload = response['Payload'].read()
    print(response_payload.decode('utf-8'))  # Print or process the response as needed

    processed = response_payload.decode('utf-8')
    dictionary = json.loads(processed)
    body = dictionary.get("body")
    print(body)
    return body


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """
    start_time = datetime.now()
    # GET
    # querystring = event.get('queryStringParameters', event)
    # mp3_base64 = querystring.get('mp3')

    # for POST
    # body = event.get('body', event)
    # print(event)
    # print(body)
    # mp3_base64 = body.get('mp3')
    mp3_base64 = event.get('mp3')

    # body = event.get('body', '{}')
    # payload = json.loads(body)
    # mp3_base64 = payload.get('mp3')

    # batch_size = int(querystring.get('batch', 16))

    # print(f"event: {event}")
    os.system("rm -rf /tmp/*")

    with TemporaryDirectory() as tmp_dir:
        os.chdir(tmp_dir)

        mp3_file = 'temporary.mp3'

        try:
            # Decode Base64
            decoded_data = base64.b64decode(mp3_base64)

            with open(mp3_file, 'wb') as f:
                f.write(decoded_data)

            print("MP3 file successfully created:", mp3_file)
        except Exception as e:
            print("Error:", e)

        output_test_dir = Path(tmp_dir)

        output_path = output_test_dir / mp3_file
        output_path = str(output_path)
        multithreading_sampling(mp3_file, output_path, num_samples_per_song=16, y_parameter=250,
                                max_workers=1, sample_duration=5) # or was it 10 seconds??

        test_ims = list(output_test_dir.glob('*.png'))

        # upload mp3 to s3
        current_time = start_time.strftime('%Y%m%d_%H%M%S%f')
        s3_key = f"{current_time}.mp3"
        s3 = boto3.client('s3')
        s3.upload_file(mp3_file, "musicclassifierspectrograms", s3_key)

        # upload spectrograms to s3
        image_paths_in_s3 = []
        for i, im in enumerate(test_ims):
            s3_key = f"{current_time}_im{i}.png"
            s3.upload_file(im, "musicclassifierspectrograms", s3_key)
            image_paths_in_s3.append(s3_key)


        ## Database info
        end_time = datetime.now()
        time_elapsed = end_time - start_time
        time_in_ms = (time_elapsed.seconds * 1000) + \
                     (time_elapsed.microseconds / 1000)
        print(time_elapsed)

        user_id = str(uuid.uuid4())


        ## invoking second lambda

        function_name = 'musicinference-HelloWorldFunction-MNqtiDedAWpz'

        payload = {
            'queryStringParameters': {
                'im_s3_list': image_paths_in_s3,
            }
        }

        result = invoke_second_lambda(function_name, payload)

        print(result)
        print(type(result))



        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",  # Change this to your specific allowed origins
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            },
            "body": json.dumps({
                "Spectrogram_paths": image_paths_in_s3
            }),
        }


if __name__ == "__main__":
    with open(os.getenv("TXT_PATH", '/Users/joannazhang/Downloads/base64.txt'), 'r') as f:
        b64_mp3 = f.read()
    print(len(b64_mp3))
    # lambda_handler({"body": {"mp3": b64_mp3}}, None)