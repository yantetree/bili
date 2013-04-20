import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import sys
import os

app_path = os.path.join(os.path.dirname(__file__), '..')
if app_path not in sys.path:
    sys.path.append(app_path)

from bili.config import *
from bili.handlers.tests import *
from bili.handlers.main import *
from bili.models import *
from bili.utils.store import RedisStore
from bili.utils.config_parser import config_parser
from sqlalchemy.orm import scoped_session, sessionmaker
from tornado.options import define, options

try:
    import redis
except ImportError:
    print "`redis` package is required"
    sys.exit(0)

   
define("port", default=8888, help="run on the given port", type=int)
    
class Application(tornado.web.Application):
    '''
    Inherit the original Application class.
    Add global connection to redis and database.
    '''
    def __init__(self):
        handlers = [
            (r"/", tornado.web.RedirectHandler, dict(url="/home")),
            (r"/home", HomeHandler),
            (r"/test/session", TestSession),
            (r"/test/register", TestRegister),
            (r"/test/login", TestLogin),
            (r"/test/logout", TestLogout),
        ]
        settings = {
                "template_path": os.path.join(os.path.dirname(__file__), 
                    "templates"),
                "static_path": os.path.join(os.path.dirname(__file__), "statics"),
                "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
                "xsrf_cookies": True,
                "login_url": "/login",
                "configs": ["config.py",]
        }
        files = [open(config_file) for config_file in settings["configs"]]
        config_parser(files, settings)
        for f in files:
            f.close()
        tornado.web.Application.__init__(self, handlers, **settings)
        self.store = RedisStore(redis.Redis(host=settings['REDIS']['HOST'], 
                port=int(settings['REDIS']['PORT'])))
        # use scoped_session to make it a thread-local variable
        self.db = scoped_session(sessionmaker(bind=engine))


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    print "Server starts at port %d" % options.port
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()

