# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys
# import sphinx_rtd_theme
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('../'))
sys.path.insert(0, os.path.abspath('../../'))
sys.path.insert(0, os.path.abspath('../pyoshub/'))
sys.path.insert(0, os.path.abspath('../../pyoshub/'))
sys.path.insert(0, os.path.abspath('../../pyoshub/pyoshub/'))
# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'pyoshub'
copyright = '2022, Open Apparel Registry'
author = 'Klaus G. Paul'
version = '0.4.4'
release = '0.4.4'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinxcontrib.plantuml',
    'sphinx.ext.autosectionlabel',
    'sphinx_copybutton',
    # 'numpydoc'
]

templates_path = ['_templates']
exclude_patterns = []

source_suffix = '.rst'
master_doc = 'index'
pygments_style = 'sphinx'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# htmlhelp_basename = 'simplebledoc'
autodoc_mock_imports = ['requests', 'pyyaml', 'pandas', 'yaml']

napoleon_google_docstring = False
napoleon_numpy_docstring = True

# autoclass_content = 'both'

autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '_flatten_facilities_json'
}
