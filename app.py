from flask import Flask, session, g
import config
from exts import db, mail
from main import user_bp
from main import item_bp
from flask_migrate import Migrate
from models import UserModel
import logging
from logging.handlers import TimedRotatingFileHandler


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(user_bp)
app.register_blueprint(item_bp)

# hook
# before_request / before_first_request/ after_request

# request -> before_request -> views -> models in views -> context_processor


@app.before_request
def before_request():
    user_id = session.get("user_id")
    if user_id:
        user = UserModel.query.get(user_id)
        # combined g with a variety called user and the value is user
        setattr(g, "user", user)
    else:
        setattr(g, "user", None)


@app.context_processor
def context_processor():
    return {"user": g.user}


if __name__ == "__main__":
    formatter = logging.Formatter("[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s][%(thread)d] - %(message)s")
    handler = TimedRotatingFileHandler(
        "flask.log", when="D", interval=1, backupCount=15,
        encoding="UTF-8", delay=False, utc=True)
    app.logger.addHandler(handler)
    handler.setFormatter(formatter)
    app.run()  # run in local
    # app.run(host="0.0.0.0")  # deployment
