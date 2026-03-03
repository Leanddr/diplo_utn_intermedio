# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# -- Path setup --------------------------------------------------------------
# Agregamos el directorio padre para que Sphinx encuentre los módulos Python
sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------
# Información del proyecto

project = 'App Estacionamiento'
copyright = '2026, Diplomatura UTN - Python Intermedio'
author = 'Leandro Romero - DNI 33028043'
release = '1.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',      # Genera documentación desde docstrings
    'sphinx.ext.viewcode',     # Agrega links al código fuente
    'sphinx.ext.napoleon',     # Soporta docstrings estilo Google/NumPy
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Idioma de la documentación
language = 'es'

# -- Options for HTML output -------------------------------------------------

html_theme = 'alabaster'  # Tema simple y limpio
html_static_path = ['_static']

# -- Options for autodoc -----------------------------------------------------
# Configuración para que autodoc extraiga bien los docstrings

autodoc_member_order = 'bysource'  # Ordenar por orden en el código
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'show-inheritance': True,
}
