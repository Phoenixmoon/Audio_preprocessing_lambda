# Path to dockerfile
$docker_file = "Dockerfile"
# ECR uri
$ecr = "608506721320.dkr.ecr.us-east-1.amazonaws.com"
# Name of the repository
$container_name = "/audio_preprocessing_lambda"
# Tag name for the latest version of the image
$tag = "latest"

$full_uri = $ecr + $container_name + ":" + $tag

# Build the image
docker build -t $full_uri -f $docker_file .
# Login
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $ecr
# Push the image to ECR
docker push $full_uri