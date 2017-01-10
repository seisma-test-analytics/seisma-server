# -*- coding: utf-8 -*-

from flask import Blueprint as _Blueprint

from .. import constants


class ViewBlueprint(_Blueprint):

    def __init__(self, name, *args, **kwargs):
        kwargs.update(
            import_name=name,
            static_url_path='/docs',
            static_folder=constants.DOCS_FOLDER,
            template_folder=constants.FRONTEND_FOLDER,
        )

        super(ViewBlueprint, self).__init__(name, *args, **kwargs)
