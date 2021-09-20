install:
	pip install -e .
	cd client; npm install
format:
	autopep8 . -r -i
	black . -l 79
debug-client:
	cd client; npm start
debug-server:
	FLASK_APP=main.py FLASK_DEBUG=1 flask run
deploy:
	rm -rf policy_engine/static
	cd client; npm run build
	cp -r client/build policy_engine/static
	echo "Deployment not yet setup"
test:
	pytest tests -vv
deploy-local: test
	rm -rf policy_engine/static
	cd client; npm run build
	cp -r client/build server/static
	FLASK_APP=main.py FLASK_DEBUG=1 flask run