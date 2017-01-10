# -*- coding: utf-8 -*-

import flask

from ... import constants
from ..base import ViewBlueprint


blueprint = ViewBlueprint(__name__)


@blueprint.route('/', methods=['GET'])
def index():
    return flask.render_template(
        constants.INDEX_HTML_FILE,
    )


@blueprint.route('/docs/', methods=['GET'])
def docs():
    return flask.redirect('/docs/index.html', code=302)
