#!/bin/bash
set -e

# Registry namespace
REGISTRY="blsq"

IMAGES=(
"postgres"
"redis"
"mcuadros/ofelia"
"memcached"
"minio/mc"
"minio/minio"
"netdata/netdata"
"portainer/portainer-ce"
"traefik"
"restic/restic"
)

# List images
echo "List of images:"
for i in "${!IMAGES[@]}"; do
  echo "$i - ${IMAGES[$i]}"
done

# Choose an image
read -p "Enter image number to copy: " CHOICE

IMAGE="${IMAGES[$CHOICE]}"

# Choose tag 
read -p "Enter tag for $IMAGE (leave empty to use latest): " INPUT_TAG

if [ -z "$INPUT_TAG" ]; then
  TAG="latest"
else
  TAG="$INPUT_TAG"
fi

SOURCE_IMAGE="$IMAGE:$TAG"

# Pull image
echo "Pulling $SOURCE_IMAGE"
docker pull "$SOURCE_IMAGE"

# If latest generate release date tag
if [ "$TAG" = "latest" ]; then
  CREATED=$(docker inspect "$SOURCE_IMAGE" --format '{{.Created}}' | sed 's/\..*Z/Z/' | tr ':T' '-_')
  TARGET_TAG="release-${CREATED}"
else
  TARGET_TAG="$TAG"
fi

# Target image
TARGET_IMAGE="${REGISTRY}/$(basename "$IMAGE"):$TARGET_TAG"

# Tag
echo "Tagging $TARGET_IMAGE"
docker tag "$SOURCE_IMAGE" "$TARGET_IMAGE"

# Push
echo "Pushing $TARGET_IMAGE"
docker push "$TARGET_IMAGE"

echo "Done"