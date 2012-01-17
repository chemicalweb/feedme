# -*- coding: utf-8 -*-

from feedme.views.main import main, IndexView

routes = [
    ((main, ''),
        ('/', IndexView.as_view('index')),
    ),
]
