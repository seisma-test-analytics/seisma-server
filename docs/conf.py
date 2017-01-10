# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__name__),
            '../',
        ),
    ),
)

import shlex

import alabaster


from seisma import wsgi


sys.path.insert(0, os.path.abspath('..'))


extensions = [
    'alabaster',
    'sphinx.ext.pngmath',
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinxcontrib.httpdomain',
]

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'

project = u'seisma'
copyright = u'2016, M.Trifonov'
author = u'M.Trifonov'

version = '0.1.x'
release = '0.1.x'

language = None
exclude_patterns = ['_build']
pygments_style = 'sphinx'
todo_include_todos = False

html_theme = 'alabaster'
html_theme_path = [
    alabaster.get_path(),
]
html_theme_options = {
    # 'logo': 'logo.png',
    'logo_name': 'seisma',
    'description': 'Test analitic system',
    'github_button': False,
    'github_banner': True,
    'show_powered_by': False,
    'github_user': 'trifonovmixail',
    'github_repo': 'seisma',
}
html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',
        'searchbox.html',
        'donate.html',
    ],
}

html_static_path = ['_static']
htmlhelp_basename = 'seismadoc'

latex_elements = {}
latex_documents = [
  (master_doc, 'seisma.tex', u'seisma Documentation',
   u'M.Trifonov', 'manual'),
]

man_pages = [
    (master_doc, 'seisma', u'seisma Documentation',
     [author], 1)
]

texinfo_documents = [
  (master_doc, 'seisma', u'seisma Documentation',
   author, 'seisma', 'One line description of project.',
   'Miscellaneous'),
]
