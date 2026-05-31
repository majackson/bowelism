# Bowelism

Personal website at https://mattjackson.uk. The site's defining feature is that it streams its own nginx access logs back to the page over a websocket — the "guts" of the server are deliberately exposed in the frontend, in the spirit of the [Bowelism](https://en.wikipedia.org/wiki/Bowellism) architectural style.

## Security note

Streaming server logs to the public frontend is the entire point of the project, not an oversight. Conventional security guidance against exposing logs does not apply here — exposure is the design. Be mindful of this when changing what gets logged or what fields appear in `STREAMED_LOG_FILE`: anything that ends up in that file becomes public.

Do not propose changes that "lock down" log exposure, suppress lines, or add auth around the log websocket unless explicitly asked. Treat the access log as user-facing content.

## Architecture

Five containers, orchestrated by `docker-compose.yml`. Both development and production run via Docker Compose (production deployment is not robust, but it's what we use for now):

- **web** — Django under uWSGI, serves the HTML page.
- **web-asgi** — Django under Daphne, terminates the log-streaming websocket.
- **log-producer** — `python manage.py log_producer`; watches `$STREAM_PATH/$STREAMED_LOG_FILE` with `watchdog` + `pygtail` and pushes new lines into the channel layer.
- **redis** — channel layer backend for `channels-redis`.
- **server** — nginx; routes `/ws/` to Daphne, everything else to uWSGI, serves static assets directly. Its own access log is the file the log-producer tails.

The loop closes on itself: requests hit nginx → nginx writes a log line → log-producer picks it up → broadcast via redis → consumers send to all open sockets → the browser appends the line.

## Key code locations

- `bowelism/settings.py` — base settings. `STREAMED_LOG_PATH`, `STREAMED_LOG_FILE`, `STREAMING_LOG_GROUP` are the log-streaming knobs.
- `bowelism/settings_production.py` — loaded when `PRODUCTION=1`. Switches to Postgres, S3 staticfiles, SES email.
- `bowelism/routing.py` + `bowelism/log_streaming/routing.py` — ASGI/websocket URL config.
- `bowelism/log_streaming/consumers.py` — `LogStreamingConsumer`. On connect, sends the last 60 lines of the log file directly (read from disk, not via the channel layer). Subsequent lines arrive via `log_lines` group messages.
- `bowelism/log_streaming/management/commands/log_producer.py` — the tailer. Runs as its own container.
- `bowelism/log_streaming/views.py` + `bowelism/urls.py` — the page itself is one view serving `index.html` with a `content` flag for which section to show.
- `bowelism/templates/index.html` — contains the frontend JS for the log stream (inline `<script>` block).
- `bowelism/api/` — only contains the `/heartbeat/` endpoint for monitoring.

## Development

```bash
make bootstrap   # first-time setup: copy .env.template, build images, collect static
make run         # docker compose up with DEBUG=TRUE and ADMIN=TRUE
make serve       # docker compose up -d (detached)
make shell       # Django shell in the web container
make django DJANGO_CMD=migrate   # arbitrary manage.py commands
```

Tests use `pytest` + `pytest-django` (see `pytest.ini`, `tests/`). Lint with `flake8` (config in `.flake8`).

## JavaScript style

The frontend JS lives inline in Django templates (currently just `index.html`). It follows a specific style — match it when adding new JS:

- **One namespaced object per concern**, attached to `document` (e.g. `document.log_streaming = { ... }`). No loose top-level state.
- **Configuration constants live as `SCREAMING_SNAKE_CASE` properties at the top of the object** (`LOG_STREAM_URI`, `TEMPLATE_CLASS`, `SECTION_CLASSES`, …). State that gets populated later (DOM refs, sockets) is declared in the same object and initialised to `null`.
- **Methods use object-literal syntax** — `init: function() { ... }` — not method shorthand (`init() { ... }`) and not arrow methods. `this` inside refers to the namespace object.
- **`snake_case` for methods and variables** (`received_log_line`, `log_lines_container`, `active_section`). This intentionally matches the Python side.
- **Arrow functions for callbacks and event handlers** so `this` keeps pointing at the namespace object (`socket.onmessage = e => { this.received_log_lines(...) }`).
- **`let` and `const` over `var`** — `var` is out (clearer scoping rules). `const` is fine for values that aren't reassigned; `let` when they are. Don't force `const` everywhere.
- **DOM access via the classic APIs** — `getElementById`, `getElementsByClassName`. Don't introduce jQuery or a framework.
- **Wire-up at the bottom of the script**: `document.addEventListener("DOMContentLoaded", () => document.<namespace>.init())`, plus any other top-level event listeners.

See the existing block in `bowelism/templates/index.html` as the reference example.

## Environment variables

- `DEBUG`, `ADMIN`, `PRODUCTION` — booleans (any truthy string enables them).
- `STREAM_PATH` — host path mounted into `log-producer` and `web-asgi` at `/source_path`. Must contain the file named by `STREAMED_LOG_FILE` (default `access.log`).
- Production extras: `AWS_DEFAULT_REGION`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `DATABASE_HOST`/`PORT`/`NAME`/`USER`/`PASSWORD`.

## Conventions

- Python: 4-space indent, `flake8` clean. Snake_case throughout.
- Routes use `re_path` (not `path`) — keep that consistent.
- The site has no real database models (`bowelism/api/models.py` is empty); don't add migrations or ORM code unless a feature genuinely needs persistence.
