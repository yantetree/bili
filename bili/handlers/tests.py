from bili.auth import login, logout, register
from bili.utils.session import session
from bili.utils.store import DictStore
from tornado import web

__all__ = ['TestSession', 'TestLogin', 'TestLogout', 'TestRegister']

class TestSession(web.RequestHandler):
    @session
    def get(self):
        session_id = self.get_secure_cookie("session_id")
        print session_id
        print self.session.get("test")
        self.session.set("test", 123)
        self.application.store.delete(session_id)

class TestRegister(web.RequestHandler):
    @session
    def get(self):
        return self.render("tests/test_register.html")
    def post(self):
        username = self.get_argument('u')
        email = self.get_argument('e')
        password = self.get_argument('p')
        user = register(self, username, email, password)
        if user:
            self.write('Success')
        else:
            self.write('Fail')
        
class TestLogin(web.RequestHandler):
    @session
    def get(self):
        return self.render("tests/test_login.html")

    @session
    def post(self):
        account = self.get_argument('u')
        password = self.get_argument('p')
        user = login(self, account, password)
        if user:
            self.write('Success')
        else:
            self.write('Fail')


class TestLogout(web.RequestHandler):
    @session
    def get(self):
        logout(self)
