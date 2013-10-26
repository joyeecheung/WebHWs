import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)

class item:
  def __init__(self, name, filetype, size):
    self.name = name
    self.filetype = filetype;
    if size < 1024:
      self.size = "%d b" % size
    elif size < 1024 * 1024:
      self.size = "%d kb" % (size/1024)
    else:
      self.size = "%d mb" % (size/(1024*1024))

class IndexHandler(tornado.web.RequestHandler):
  def get(self):
    playlist = self.get_argument('playlist', 'None')
    filepath = os.path.join(os.path.dirname(__file__), "static/songs")
    filenames = os.listdir(filepath)

    files = [];
    if playlist is not 'None':
      listfile = open(os.path.join(filepath, playlist))
      filenames = listfile.read().splitlines()

    for filename in filenames:
      files.append(item(filename,
                        os.path.splitext(filename)[1][1:],
                        os.path.getsize(os.path.join(filepath, filename))
                  ))
    files.sort(key=lambda x:(x.filetype, x.name))
    self.render('music.html', files=files)

if __name__ == '__main__':
  tornado.options.parse_command_line()
  app = tornado.web.Application(
    handlers=[(r'/', IndexHandler)],
    template_path=os.path.join(os.path.dirname(__file__), "template"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    debug=True
    )
  http_server = tornado.httpserver.HTTPServer(app)
  http_server.listen(options.port)
  tornado.ioloop.IOLoop.instance().start()