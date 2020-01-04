APPNAME=di-vita
TAG=latest


fetch:
	python di-vita.py

docker-image:
	docker build --rm --tag ${APPNAME}:${TAG} .

docker-run: docker-image
	docker run ${APPNAME}:${TAG}