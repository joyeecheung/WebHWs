import cardValidate

import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        error = self.get_argument('error', None)
        if error == 'incomplete':
            self.render('error.html', error_msg="You didn't fill the form completely.")
        elif error == 'wrongcard':
            self.render('error.html', error_msg="You didn't provide a valid card number.")
        else:
            self.render('buyagrade.html')

    def post(self):
        name = self.get_argument('name', None)
        section = self.get_argument('section', None)
        card = self.get_argument('card', None)
        card_type = self.get_argument('card_type', None)

        if not name or not section or not card or not card_type:
            self.redirect('/?error=incomplete')
        elif not cardValidate.IsValid(card, card_type):
            self.redirect('/?error=wrongcard')
        else:
            current = dict()
            current['name'] = name
            current['section'] = section
            current['card'] = card.replace('-', '')
            current['card_type'] = card_type

            f = open(os.path.join(os.path.dirname(__file__),
                                'static', 'data', 'suckers.txt'), 'r')
            suckers = f.read()
            f.close()

            f = open(os.path.join(os.path.dirname(__file__),
                                'static', 'data', 'suckers.txt'), 'a')

            f.write(';'.join([name, section, card, card_type]))
            f.write('\n')
            f.close()
            self.render('sucker.html', current=current, suckers=suckers)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
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