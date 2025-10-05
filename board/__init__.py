import os
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        FLASK_DATABASE=os.path.join(app.instance_path, 'board.sqlite'),
    )
    
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import pages, posts, database

    app.register_blueprint(pages.bp)
    app.register_blueprint(posts.bp)

    database.init_app(app)

    return app
