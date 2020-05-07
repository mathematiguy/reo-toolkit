DOCKER_REGISTRY := 473856431958.dkr.ecr.ap-southeast-2.amazonaws.com
IMAGE_NAME := $(shell basename `git rev-parse --show-toplevel` | tr '[:upper:]' '[:lower:]')
IMAGE := $(DOCKER_REGISTRY)/$(IMAGE_NAME)
HAS_AWS = $(shell which aws)
HAS_DOCKER = $(shell which docker)
RUN ?= $(if $(HAS_DOCKER), docker run $(DOCKER_ARGS) -t --rm -v $$(pwd):/code -w /code -u $(UID):$(GID) $(IMAGE))
UID ?= $(shell id -u)
GID ?= $(shell id -g)
DOCKER_ARGS ?= 
GIT_TAG ?= $(shell git log --oneline | head -n1 | awk '{print $$1}')
NUM_CORES ?= $(shell expr `grep -c ^processor /proc/cpuinfo` - 1)
MULTICORE ?=
LOG_LEVEL ?= DEBUG

.PHONY: test jupyter docker-login docker docker-push docker-pull enter enter-root

test:
	$(RUN) bash -c "coverage run --source reo_toolkit -m pytest -vv $(if $(MULTICORE), -n $(NUM_CORES)) --durations 10 --log-level $(LOG_LEVEL) && coverage report"

daemon: DOCKER_ARGS= -dit --rm -e DISPLAY=$$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix:ro --name="rdev"
daemon:
	$(RUN) R

JUPYTER_PASSWORD ?= jupyter
JUPYTER_PORT ?= 8888
jupyter: UID=root
jupyter: GID=root
jupyter: DOCKER_ARGS=-u $(UID):$(GID) --rm -it -p $(JUPYTER_PORT):$(JUPYTER_PORT) -e NB_USER=$$USER -e NB_UID=$(UID) -e NB_GID=$(GID)
jupyter:
	$(RUN) jupyter lab \
		--allow-root \
		--port $(JUPYTER_PORT) \
		--ip 0.0.0.0 \
		--NotebookApp.password=$(shell $(RUN) \
			python3 -c \
			"from IPython.lib import passwd; print(passwd('$(JUPYTER_PASSWORD)'))")

PROFILE ?= default
docker-login:
	$(if $(HAS_AWS), eval $$(aws ecr get-login --no-include-email --profile $(PROFILE) --region ap-southeast-2 | sed 's|https://||'))

docker: docker-login
	docker build $(DOCKER_ARGS) --tag $(IMAGE):$(GIT_TAG) .
	docker tag $(IMAGE):$(GIT_TAG) $(IMAGE):latest

docker-push:
	docker push $(IMAGE):$(GIT_TAG)
	docker push $(IMAGE):latest

docker-pull:
	docker pull $(IMAGE):$(GIT_TAG)
	docker tag $(IMAGE):$(GIT_TAG) $(IMAGE):latest

enter: DOCKER_ARGS=-i
enter:
	$(RUN) bash

enter-root: DOCKER_ARGS=-i
enter-root: UID=root
enter-root: GID=root
enter-root:
	$(RUN) bash

