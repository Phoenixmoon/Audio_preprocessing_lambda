# Audio Preprocessing Lambda

Takes the mp3 base64 sent from the website as input, converts it back to audio and then an array, generates spectrogram array, using random sampling to produce 16 10-second cropped spectrogram images which are then uploaded to s3. The s3 keys are returned to be passed on to the second inference lambda. 

[//]: # (To build docker images &#40;tag and then . to refer to docker image&#41;)

To build docker images:
```bash
docker build --no-cache -t 851633384945.dkr.ecr.us-east-2.amazonaws.com/test_ecr:v4 . 
# or
docker build -t 851633384945.dkr.ecr.us-east-1.amazonaws.com/test_ecr:v10 .
```

Docker push:

[//]: # (aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 851633384945.dkr.ecr.us-east-2.amazonaws.com
docker push 851633384945.dkr.ecr.us-east-2.amazonaws.com/test_ecr:v4
docker tag public.ecr.aws/n8c6o8k7/audio_preprocessing_image:latest 851633384945.dkr.ecr.us-east-1.amazonaws.com/test_ecr:harry
)

```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 851633384945.dkr.ecr.us-east-1.amazonaws.com
docker push 851633384945.dkr.ecr.us-east-1.amazonaws.com/test_ecr:v10
```

docker pull
```bash
docker pull 851633384945.dkr.ecr.us-east-1.amazonaws.com/test_ecr:v11
```

## Run Docker:

```
docker run -dit --platform linux/amd64 -v /Users/joannazhang/Downloads:/joannazhang/Downloads -v /Users/joannazhang/.aws:/root/.aws -e TXT_PATH=/joannazhang/Downloads/base64.txt 851633384945.dkr.ecr.us-east-1.amazonaws.com/test_ecr:v11
docker run -dit -v /Users/joannazhang/Downloads:/joannazhang/Downloads -v /Users/joannazhang/.aws:/root/.aws -e TXT_PATH=/joannazhang/Downloads/base64.txt 851633384945.dkr.ecr.us-east-1.amazonaws.com/test_ecr:v11
```

This project contains source code and supporting files for a serverless application deployed with the SAM CLI. It includes the following files and folders.

- hello_world - Code for the application's Lambda function (app.py) and Project Dockerfile, as well as helper functions (found in spectrogram_generation_functions.py).

[//]: # (- events - Invocation events that you can use to invoke the function.)
[//]: # (- tests - Unit tests for the application code. )
- template.yaml - A template that defines the application's AWS resources.

The application uses several AWS resources, including Lambda functions and an API Gateway API. These resources are defined in the `template.yaml` file in this project. You can update the template to add AWS resources through the same deployment process that updates your application code.

[//]: # ()
[//]: # (## Deploy the sample application)

[//]: # ()
[//]: # (The Serverless Application Model Command Line Interface &#40;SAM CLI&#41; is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that matches Lambda. It can also emulate your application's build environment and API.)

[//]: # ()
[//]: # (To use the SAM CLI, you need the following tools.)

[//]: # ()
[//]: # (* SAM CLI - [Install the SAM CLI]&#40;https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html&#41;)

[//]: # (* Docker - [Install Docker community edition]&#40;https://hub.docker.com/search/?type=edition&offering=community&#41;)

[//]: # ()
[//]: # (You may need the following for local testing.)

[//]: # (* [Python 3 installed]&#40;https://www.python.org/downloads/&#41;)

[//]: # ()
[//]: # (To build and deploy your application for the first time, run the following in your shell:)

[//]: # ()
[//]: # (```bash)

[//]: # (sam build)

[//]: # (sam deploy --guided)

[//]: # (```)

[//]: # ()
[//]: # (The first command will build a docker image from a Dockerfile and then copy the source of your application inside the Docker image. The second command will package and deploy your application to AWS, with a series of prompts:)

[//]: # ()
[//]: # (* **Stack Name**: The name of the stack to deploy to CloudFormation. This should be unique to your account and region, and a good starting point would be something matching your project name.)

[//]: # (* **AWS Region**: The AWS region you want to deploy your app to.)

[//]: # (* **Confirm changes before deploy**: If set to yes, any change sets will be shown to you before execution for manual review. If set to no, the AWS SAM CLI will automatically deploy application changes.)

[//]: # (* **Allow SAM CLI IAM role creation**: Many AWS SAM templates, including this example, create AWS IAM roles required for the AWS Lambda function&#40;s&#41; included to access AWS services. By default, these are scoped down to minimum required permissions. To deploy an AWS CloudFormation stack which creates or modifies IAM roles, the `CAPABILITY_IAM` value for `capabilities` must be provided. If permission isn't provided through this prompt, to deploy this example you must explicitly pass `--capabilities CAPABILITY_IAM` to the `sam deploy` command.)

[//]: # (* **Save arguments to samconfig.toml**: If set to yes, your choices will be saved to a configuration file inside the project, so that in the future you can just re-run `sam deploy` without parameters to deploy changes to your application.)

[//]: # ()
[//]: # (You can find your API Gateway Endpoint URL in the output values displayed after deployment.)

[//]: # ()
[//]: # (## Use the SAM CLI to build and test locally)

[//]: # ()
[//]: # (Build your application with the `sam build` command.)

[//]: # ()
[//]: # (```bash)

[//]: # (untitled1$ sam build)

[//]: # (```)

[//]: # ()
[//]: # (The SAM CLI builds a docker image from a Dockerfile and then installs dependencies defined in `hello_world/requirements.txt` inside the docker image. The processed template file is saved in the `.aws-sam/build` folder.)

[//]: # ()
[//]: # (Test a single function by invoking it directly with a test event. An event is a JSON document that represents the input that the function receives from the event source. Test events are included in the `events` folder in this project.)

[//]: # ()
[//]: # (Run functions locally and invoke them with the `sam local invoke` command.)

[//]: # ()
[//]: # (```bash)

[//]: # (untitled1$ sam local invoke HelloWorldFunction --event events/event.json)

[//]: # (```)

[//]: # ()
[//]: # (The SAM CLI can also emulate your application's API. Use the `sam local start-api` to run the API locally on port 3000.)

[//]: # ()
[//]: # (```bash)

[//]: # (untitled1$ sam local start-api)

[//]: # (untitled1$ curl http://localhost:3000/)

[//]: # (```)

[//]: # ()
[//]: # (The SAM CLI reads the application template to determine the API's routes and the functions that they invoke. The `Events` property on each function's definition includes the route and method for each path.)

[//]: # ()
[//]: # (```yaml)

[//]: # (      Events:)

[//]: # (        HelloWorld:)

[//]: # (          Type: Api)

[//]: # (          Properties:)

[//]: # (            Path: /hello)

[//]: # (            Method: get)

[//]: # (```)

[//]: # ()
[//]: # (## Add a resource to your application)

[//]: # (The application template uses AWS Serverless Application Model &#40;AWS SAM&#41; to define application resources. AWS SAM is an extension of AWS CloudFormation with a simpler syntax for configuring common serverless application resources such as functions, triggers, and APIs. For resources not included in [the SAM specification]&#40;https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md&#41;, you can use standard [AWS CloudFormation]&#40;https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html&#41; resource types.)

[//]: # ()
[//]: # (## Fetch, tail, and filter Lambda function logs)

[//]: # ()
[//]: # (To simplify troubleshooting, SAM CLI has a command called `sam logs`. `sam logs` lets you fetch logs generated by your deployed Lambda function from the command line. In addition to printing the logs on the terminal, this command has several nifty features to help you quickly find the bug.)

[//]: # ()
[//]: # (`NOTE`: This command works for all AWS Lambda functions; not just the ones you deploy using SAM.)

[//]: # ()
[//]: # (```bash)

[//]: # (untitled1$ sam logs -n HelloWorldFunction --stack-name "untitled1" --tail)

[//]: # (```)

[//]: # ()
[//]: # (You can find more information and examples about filtering Lambda function logs in the [SAM CLI Documentation]&#40;https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-logging.html&#41;.)

[//]: # ()
[//]: # (## Unit tests)

[//]: # ()
[//]: # (Tests are defined in the `tests` folder in this project. Use PIP to install the [pytest]&#40;https://docs.pytest.org/en/latest/&#41; and run unit tests from your local machine.)

[//]: # ()
[//]: # (```bash)

[//]: # (untitled1$ pip install pytest pytest-mock --user)

[//]: # (untitled1$ python -m pytest tests/ -v)

[//]: # (```)

[//]: # ()
[//]: # (## Cleanup)

[//]: # ()
[//]: # (To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:)

[//]: # ()
[//]: # (```bash)

[//]: # (sam delete --stack-name "untitled1")

[//]: # (```)

[//]: # ()
[//]: # (## Resources)

[//]: # ()
[//]: # (See the [AWS SAM developer guide]&#40;https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html&#41; for an introduction to SAM specification, the SAM CLI, and serverless application concepts.)

[//]: # ()
[//]: # (Next, you can use AWS Serverless Application Repository to deploy ready to use Apps that go beyond hello world samples and learn how authors developed their applications: [AWS Serverless Application Repository main page]&#40;https://aws.amazon.com/serverless/serverlessrepo/&#41;)
