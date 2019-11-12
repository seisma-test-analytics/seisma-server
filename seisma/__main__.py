# -*- coding: utf-8 -*-

from flask_script import Manager
from flask_migrate import Migrate
from flask_migrate import MigrateCommand

from seisma import wsgi
from seisma import constants
from seisma.database.alchemy import alchemy

from seisma.commands.clean import CleanCommand
from seisma.commands.rotate import RotateCommand
from seisma.commands.fix_aborted import FixAbortedBuilds
from seisma.commands.fixtures import UploadFixturesToDatabase


manager = Manager(wsgi.app)
migrate = Migrate(wsgi.app, alchemy, directory=constants.MIGRATE_DIR)


manager.add_command('db', MigrateCommand)
manager.add_command('clean', CleanCommand)
manager.add_command('rotate', RotateCommand)
manager.add_command('fix_aborted', FixAbortedBuilds)
manager.add_command('load_fixtures', UploadFixturesToDatabase)


if __name__ == '__main__':
    manager.run()
