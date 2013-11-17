"""Tornado server configuration."""
import os.path
from items import MovieInfo, Reviews

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)

class ReviewsModule(tornado.web.UIModule):
    """UI Module for review columns."""
    def render(self, review_items):
        return self.render_string('modules/review.html',
                                  review_items=review_items)

class IndexHandler(tornado.web.RequestHandler):
    """Handler for root page."""
    def get(self):
        film = self.get_argument('film')
        filepath = os.path.join(os.path.dirname(__file__),
                                'static', 'movies', film)

        # get movie info from info.txt
        movie_info = MovieInfo(filepath)

        # get general overview from generaloverview.txt
        overview_file = open(os.path.join(filepath, 'generaloverview.txt'))

        overview = list()
        for line in overview_file:
            line = line.strip()
            (term, sep, data) = line.partition(':')
            overview.append((term, data))

        # get reviews from review[0-9]*.txt
        reviews = Reviews(filepath)

        self.render('movie.html', movie_info=movie_info, overview=overview,
                                reviews=reviews)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r'/', IndexHandler)],
        template_path=os.path.join(os.path.dirname(__file__), 'templates'),
        static_path=os.path.join(os.path.dirname(__file__), 'static'),
        ui_modules={'Reviews': ReviewsModule},
        debug=True
        )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
