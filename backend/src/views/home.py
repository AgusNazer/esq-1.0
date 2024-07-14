from flask import Flask, Blueprint,render_template
from src.models.user import User

home_admin = Blueprint('home', __name__)


@home_admin.route('/', methods=['GET'])
def home():
        return render_template('index.html')
        # return('sdklfklsdn ')
