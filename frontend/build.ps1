# also works in sh/bash.

# build to latest by default
# TODO look for an image host
docker build . -t cloud-storage-front
echo 'built to image cloud-storage:latest.'

# push image to 
# docker push some_host/some_user/cloud-storage-front
# echo 'docker image pushed...'