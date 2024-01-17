$containerName = "mg-front"
docker rm $containerName
docker run -p 8080:80 --name $containerName mg/front:1.0