#!/bin/bash

SOURCE_IMAGE=""
TARGET_IMAGE=""

# Pull the source image
docker pull $SOURCE_IMAGE

# Retag the image
docker tag $SOURCE_IMAGE $TARGET_IMAGE

# Push the retagged image to the target registry
docker push $TARGET_IMAGE

echo "Image $SOURCE_IMAGE has been retagged to $TARGET_IMAGE and pushed to the target registry."

# Remove both images from the local system
docker rmi $SOURCE_IMAGE
docker rmi $TARGET_IMAGE

echo "Image $SOURCE_IMAGE has been retagged to $TARGET_IMAGE, pushed to the target registry, and removed from the local system."