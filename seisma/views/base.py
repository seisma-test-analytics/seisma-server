# -*- coding: utf-8 -*-

from flask import Blueprint as _Blueprint


class ViewBlueprint(_Blueprint):

    def __init__(self, name, *args, **kwargs):
        kwargs.update(
            import_name=name,
        )

        super(ViewBlueprint, self).__init__(name, *args, **kwargs)
