# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2018 Dan Tès <https://github.com/delivrance>
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

import re
from sys import argv

from setuptools import setup

from compiler.api import compiler as api_compiler
from compiler.error import compiler as error_compiler
from compiler.docs import compiler as docs_compiler

if len(argv) > 1 and argv[1] != "sdist":
    api_compiler.start()
    error_compiler.start()
    docs_compiler.start()

# PyPI doesn't like raw html
with open("README.rst", encoding="UTF-8") as f:
    readme = re.sub(r"\.\. \|.+\| raw:: html(?:\s{4}.+)+\n\n", "", f.read())
    readme = re.sub(r"\|header\|", "|logo|\n\n|description|\n\n|scheme| |mtproto|", readme)

setup(long_description=readme)
