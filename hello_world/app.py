print('Starting import...')
import json
import librosa
import numpy as np
import boto3
import os
from datetime import datetime
from tempfile import TemporaryDirectory
import base64
from pathlib import Path
from spectrogram_generation_functions import multithreading_sampling


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

    # GET
    # querystring = event.get('queryStringParameters', event)
    # mp3_base64 = querystring.get('mp3')

    # for POST
    body = event.get('body', event)
    print(event)
    print(body)
    mp3_base64 = body.get('mp3')

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
        current_time = datetime.now().strftime('%Y%m%d_%H%M%S%f')
        s3_key = f"{current_time}.mp3"
        s3 = boto3.client('s3')
        s3.upload_file(mp3_file, "musicclassifierspectrograms", s3_key)

        # upload spectrograms to s3
        image_paths_in_s3 = []
        for i, im in enumerate(test_ims):
            s3_key = f"{current_time}_im{i}.png"
            s3.upload_file(im, "musicclassifierspectrograms", s3_key)
            image_paths_in_s3.append(s3_key)

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
    lambda_handler({"body": {"mp3": b64_mp3}}, None)