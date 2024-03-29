#docker_image_name=851633384945.dkr.ecr.us-east-1.amazonaws.com/test_image:latest

#docker build -t ${docker_image_name} .

#aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 851633384945.dkr.ecr.us-east-2.amazonaws.com
#
#docker push ${docker_image_name}


docker tag a67e27546353 851633384945.dkr.ecr.us-east-2.amazonaws.com/test_ecr
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 851633384945.dkr.ecr.us-east-2.amazonaws.com
docker push 851633384945.dkr.ecr.us-east-2.amazonaws.com/test_ecr