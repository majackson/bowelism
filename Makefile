dev-build:
	docker-compose run --name bowelism_web_cleanup --rm web bash -c "rm -rf ~/.venvs/bowelismvenv" && \
	docker-compose build

update-time:
	docker-machine ssh default "sudo ntpclient -s -h pool.ntp.org"

django:
	docker-compose run --service-ports --name bowelism_web_django --rm web bash -c "source ~/.venvs/bowelismvenv/bin/activate && python manage.py ${DJANGO_CMD}"

staticfiles:
	DJANGO_CMD="collectstatic --no-input" make django

shell:
	DJANGO_CMD=shell make django

bootstrap:
	cp -n production.env.template production.env; true && \
	make dev-build staticfiles

run:
	echo "Server will be coming up at http://`docker-machine ip`/" && \
	ADMIN=TRUE DEBUG=TRUE docker-compose up

serve:
	docker-compose start

serve-restart:
	docker-compose restart

serve-stop:
	docker-compose stop

test:
	docker-compose run --name bowelism_web_tests --rm web bash -c 'source ~/.venvs/bowelismvenv/bin/activate && py.test --strict $${TEST_ARGS:-"tests/"}'
