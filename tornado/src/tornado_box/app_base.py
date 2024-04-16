import logging
import pathlib
import tornado.web


logger = logging.getLogger(pathlib.Path(__file__).name)


class HealthzHandler(tornado.web.RequestHandler):
    def initialize(self, *, app):
        self.app = app

    def _check_health(self):
        self.set_status(202)
        self.finish()

    def head(self):
        self._check_health()

    def get(self):
        self._check_health()


class RequestPingHandler(tornado.web.RequestHandler):
    def initialize(self, *, app):
        self.app = app

    def get(self):
        logger.info("received ping, replying pong")

        self.write("pong")
        self.set_status(200)
        self.finish()


class AppBase(object):
    def __init__(
        self,
        *,
        address,
        port,
    ):
        self.address = address
        self.port = port

        self.app = self.server = None

    def _make_routes(self):
        return [
            (
                r"/healthz$",
                HealthzHandler,
                dict(app=self),
            ),
            (
                r"/ping$",
                RequestPingHandler,
                dict(app=self),
            ),
        ]

    async def start(self):
        logger.info("starting HTTP server at (%s:%s)", self.address, self.port)

        handlers = self._make_routes()
        self.app = tornado.web.Application(handlers)
        self.server = tornado.httpserver.HTTPServer(self.app, xheaders=False)
        self.server.listen(address=self.address, port=self.port)
        sockets = self.server._sockets.values()

        logger.info("listening to sockets: %s", sockets)
