setup:
	chmod +x ./setup.sh &&\
		./setup.sh
install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt
run:
	python main.py
docker:
	docker-compose up --build