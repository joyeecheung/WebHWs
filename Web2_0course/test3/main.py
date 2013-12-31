#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pymongo
import os.path
from collections import namedtuple

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

class MainPageHandler(BaseHandler):
    """Handle the main page."""
    def get(self, index):
        # retrieve data from local database
        user = self.get_current_user()
        # project user info and put it into a dict
        info_dict = self.application.db.find_one({"name": user},
            {"_id": 0, "name": 1, "image": 1, "age": 1, "email": 1})
        # get tweets of the user
        tweets = self.application.db.find_one({"name": user})['tweets']

        # Since there's only one user per page, use namedtuple
        info = namedtuple('Info', info_dict.keys())(*info_dict.values())

        self.render('twitter.html', info=info, tweets=tweets, user=user)

class LoginHandler(BaseHandler):
    """Handle the login page."""
    def get(self):
        self.render('login.html')

    def post(self):
        # retrieve the username and password in request
        user = self.get_argument('user', None)
        password = self.get_argument('password', None)

        # retrieve the user list from the database
        users = dict()
        for us in self.application.db.find():
            users[us['name']] = str(us['password'])
        print "%d users loaded." % (len(users))
        print users

        # if there's a match, set cookie then redirect
        if user in users and users[user] == password:
            self.set_secure_cookie("user", user)
            print "User " + user + " logged in."
            self.redirect('/twitter/' + user)
        else:  # if there isn't a match, back to the login page
            self.redirect('/login')

class addTweet(BaseHandler):
    """Get tweet posted with AJAX and save it to the local database."""
    def post(self):
        newTweet = tornado.escape.json_decode(self.request.body)
        user = self.get_current_user()
        record = self.application.db.find_one({"name": user})
        record['tweets'].append(newTweet)
        self.application.db.save(record)

class Application(tornado.web.Application):
    """Tornado application settings."""
    def __init__(self):
        handlers = [
            (r"/twitter/(\w+)", MainPageHandler),
            (r"/login", LoginHandler),
            (r"/ajax/addTweet", addTweet),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            debug=True,
            )
        conn = pymongo.Connection("localhost", 27017)
        twitterDB=conn["twitterDB"]
        self.db = twitterDB.userSets
        tornado.web.Application.__init__(self, handlers, **settings)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
