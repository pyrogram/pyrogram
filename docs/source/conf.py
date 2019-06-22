# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2019 Dan Tès <https://github.com/delivrance>
#
# This file is part of Pyrogram.
#
# Pyrogram is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyrogram is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys

sys.path.insert(0, os.path.abspath("../.."))

from pyrogram import __version__

from pygments.styles.friendly import FriendlyStyle

FriendlyStyle.background_color = "#f3f2f1"

project = "Pyrogram"
copyright = "2017-2019, Dan"
author = "Dan"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary"
]

master_doc = "index"
source_suffix = ".rst"
autodoc_member_order = "bysource"

version = __version__
release = version

templates_path = ["_templates"]

napoleon_use_rtype = False

pygments_style = "friendly"

html_title = "Pyrogram Documentation"
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_show_sourcelink = True
html_show_copyright = False
html_theme_options = {
    "canonical_url": "https://docs.pyrogram.org/",
    "collapse_navigation": True,
    "sticky_navigation": True,
    "logo_only": True,
    "display_version": True,
    "style_external_links": True
}

html_logo = "_images/pyrogram.png"
html_favicon = "_images/favicon.ico"

latex_engine = "xelatex"
latex_logo = "_images/pyrogram.png"

latex_elements = {
    "pointsize": "12pt",
    "fontpkg": r"""
        \setmainfont{Noto Sans}
        \setsansfont{Roboto Slab}
        \setmonofont{Ubuntu Mono}
        """
}
