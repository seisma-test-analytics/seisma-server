# -*- coding: utf-8 -*-

import flask

from ... import constants
from ..base import ViewBlueprint


blueprint = ViewBlueprint(__name__)


@blueprint.route('/', methods=['GET'])
def index():
    return flask.redirect('/docs/index.html', code=302)


@blueprint.route('/docs/<path:path>', methods=['GET'])
def docs(path):
    return flask.send_from_directory(constants.DOCS_FOLDER, path)
