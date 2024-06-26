from flask import Flask
from src.routes.user import users
from config_db import engine
from src.models.user import Base
import os

app = Flask(__name__)

app.register_blueprint(users, url_prefix='/users')

Base.metadata.create_all(bind=engine)



@app.route('/')
def hello_world():
    return 'Hello, World'

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=os.getenv("DB_PORT", default=5000))