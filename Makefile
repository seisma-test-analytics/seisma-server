MAKEFLAGS+=--silent

DOCKER=`which docker`

DOCKERFILE=Dockerfile

IMAGE_NAME=seisma/api
IMAGE_TAG?=`./ci/getVersion`

build:
	$(DOCKER) build -t $(IMAGE_NAME):$(IMAGE_TAG) -f $(DOCKERFILE) .
	$(DOCKER) tag $(IMAGE_NAME):$(IMAGE_TAG) $(IMAGE_NAME):latest

publish:
	$(DOCKER) login -u $(DOCKER_USERNAME) -p $(DOCKER_PASSWORD)
	$(DOCKER) push $(IMAGE_NAME):$(IMAGE_TAG)
	$(DOCKER) push $(IMAGE_NAME):latest
