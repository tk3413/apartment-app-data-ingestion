DOCKERUSERNAME=tk3413
APPNAME=di-vita
TAG=latest

fetch:
	python3 ${APPNAME}.py

docker-image:
	docker build --rm -t ${DOCKERUSERNAME}/${APPNAME}:${TAG} .

docker-run: docker-image
	docker run -p 3001:3001 --rm --network host --name ${APPNAME} ${DOCKERUSERNAME}/${APPNAME}:${TAG}

docker-pull:
	docker pull ${DOCKERUSERNAME}/${APPNAME}:${TAG}

docker-push: docker-image
	docker push ${DOCKERUSERNAME}/${APPNAME}:${TAG}

docker-clean:
	echo "y" | docker system prune
