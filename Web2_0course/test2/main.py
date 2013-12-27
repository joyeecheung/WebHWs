#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import data
import datetime

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)

class BaseHandler(tornado.web.RequestHandler):
    """The basic request handler with overriden functions."""
    def get_current_user(self):
        return self.get_secure_cookie("user")

    def get_error_html(self, status_code, **kwargs):
        return self.render_string("404.html",
            err=kwargs.get('message', None))

class BlogHandler(BaseHandler):
    """Handle the blog page."""
    def get(self, index):
        self.render('blog.html', blog=data.get_blog(),
                     comments=data.get_comments(),
                     user=self.get_secure_cookie("user"))

class LoginHandler(BaseHandler):
    """Handle the login page."""
    def get(self):
        self.write('<html><body><form method="post">'
                   + 'User: <input type="text" name="user">'
                   + 'Password: <input type="password" name="password">'
                   + '<input type="submit" value="Sign in">'
                   + '</form></body></html>')

    def post(self):
        user = self.get_argument('user', None)
        password = self.get_argument('password', None)

        # retrieve the user list from the database
        users = data.get_users()
        # if there's a match, set cookie then redirect
        if user in users and users[user] == password:
            self.set_secure_cookie("user", user)
            print "User " + user + " logged in."
            self.redirect('/' + user + '/Fenng/1')
        # if there's no match, send 404
        else:
            error = dict()
            error['message'] = "Wrong user name or password."
            print "Invalid user " + user + " attempted to log in."
            return self.send_error(404, **error)

class LogoutHandler(BaseHandler):
    """Handle the logout service."""
    def get(self):
        print "User " + self.get_secure_cookie("user") + " logged out."
        self.clear_cookie('user')
        self.write('Logout!')

class getComment(BaseHandler):
    def get(self):
        comments = data.get_comments()
        jsonStr = tornado.escape.json_encode(comments)

        self.set_header('Content-Type', 'application/json')
        self.write(jsonStr)
        self.finish()

class addComment(BaseHandler):
    def post(self):
        newComment = tornado.escape.json_decode(self.request.body)
        data.save_comment(newComment)

class Application(tornado.web.Application):
    """Tornado application settings."""
    def __init__(self):
        handlers = [
            (r"/(\w+)/Fenng/1", BlogHandler),
            (r"/login", LoginHandler),
            (r"/logout", LogoutHandler),
            (r"/ajax/getComment", getComment),
            (r"/ajax/addComment", addComment)
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            debug=True,
            )
        tornado.web.Application.__init__(self, handlers, **settings)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()