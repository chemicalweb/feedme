#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flaskext.script import Command, Manager

from feedme import app, db

manager = Manager(app)


class RunServer(Command):
    """Starts the application using Flask's development server."""
    def run(self):
        app.run(port=8000)


class RunTornado(Command):
    """Starts the application using the Tornado web server."""
    def run(self):
        from tornado.httpserver import HTTPServer
        from tornado.ioloop import IOLoop
        from tornado.wsgi import WSGIContainer

        http_server = HTTPServer(WSGIContainer(app))
        http_server.listen(8000, address='*')
        IOLoop.instance().start()


class SyncDB(Command):
    """Create database tables for the application's models."""
    def run(self):
        db.create_all()
        db.session.commit()


del manager._commands['runserver']
manager.add_command('runserver', RunServer())
manager.add_command('runtornado', RunTornado())
manager.add_command('syncdb', SyncDB())
manager.run()
