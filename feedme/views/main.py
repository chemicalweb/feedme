# -*- coding: utf-8 -*-

from flask import *
from flask.views import MethodView

main = Blueprint('main', __name__)


class IndexView(MethodView):
    """
    Main page's view
    """
    def get(self):
        return render_template('main/index.html')


class UpdateView(MethodView):
    def get(self):
        return redirect(url_for('main.index'))
