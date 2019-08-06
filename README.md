# Bowelism 

Small project that powers my personal website: http://mattjackson.uk.

This project was inspired by the [Bowelism](https://en.wikipedia.org/wiki/Bowellism) architectural style, in which the "guts" of a building (pipes, cabling, ducts, lift shafts) are located outside of the main structure of the building. The effect of this is maximising internal space of the building, but it also has an obvious aesthetic effect.

After reading about Bowelism, I wondered what the equivalent "bowelist" computer system might look like, with all component source code, logging, and traceback/debug data all visible from the outside. I reduced this down to just logging data, and used the concept to build my personal website. The result is this, a website which streams it's own web server logs back to the page, and displays them to the user.

When the page loads, it opens a web socket to the host, through which the last 60 lines of web server logs are streamed. Further log entries are streamed over the web socket as they occur.

The project is built with Python3, Django (and django-channels), Docker and docker-compose. It is structured as 5 Docker containers. These are:

* A Django container running uWSGI hosting the dynamically-rendered page itself.
* A Django container running Daphne for ASGI web sockets.
* A "log producer" container running a Django management task which watches the log file specified in the STREAMED_LOG_FILE environment variable, and pushes any new log lines into the Django channel.
* A redis container. Redis is used by django-channels to stream new events to the potentially numerous open web sockets.
* An nginx container forwarding the relevant requests to either the uWSGI container, the ASGI container, or serving static assets directly from itself.
