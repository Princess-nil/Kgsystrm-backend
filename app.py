from flask import Flask
import config
from exts import db, jwt, cors
from apps import graph_bp
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)
jwt.init_app(app)
cors.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(graph_bp)


if __name__ == '__main__':
    app.run()
