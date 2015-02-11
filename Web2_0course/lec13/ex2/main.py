#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pymongo
from collections import namedtuple
import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.escape

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        conn = pymongo.Connection("localhost",27017)
        db = conn["paperDB"]
        infoDB = db.infoDB
        record = infoDB.find_one()

        del record['_id']
        del record['comment']  # reserve space

        blog = namedtuple('Blog', record.keys())(*record.values())
        self.render('blog.html', blog=blog)

class getComment(tornado.web.RequestHandler):
    def get(self):
        conn = pymongo.Connection("localhost",27017)
        db = conn["paperDB"]
        infoDB = db.infoDB
        record = infoDB.find_one()
        jsonStr = tornado.escape.json_encode(record['comment'])

        self.set_header('Content-Type', 'application/json')
        self.write(jsonStr)
        self.finish()

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/ajax/getComment", getComment)
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True
            )
        tornado.web.Application.__init__(self, handlers, **settings)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()