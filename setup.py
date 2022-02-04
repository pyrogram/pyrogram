#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

import os
import re
import shutil
from sys import argv

from setuptools import setup, find_packages, Command

from compiler.api import compiler as api_compiler
from compiler.docs import compiler as docs_compiler
from compiler.errors import compiler as errors_compiler

with open("requirements.txt", encoding="utf-8") as r:
    requires = [i.strip() for i in r]

with open("pyrogram/__init__.py", encoding="utf-8") as f:
    version = re.findall(r"__version__ = \"(.+)\"", f.read())[0]

with open("README.md", encoding="utf-8") as f:
    readme = f.read()


class Clean(Command):
    DIST = ["./build", "./dist", "./Pyrogram.egg-info"]
    API = [
        "pyrogram/errors/exceptions", "pyrogram/raw/functions", "pyrogram/raw/types", "pyrogram/raw/base",
        "pyrogram/raw/all.py"
    ]
    DOCS = [
        "docs/source/telegram", "docs/build", "docs/source/api/methods", "docs/source/api/types",
        "docs/source/api/bound-methods"
    ]

    ALL = DIST + API + DOCS

    description = "Clean generated files"

    user_options = [
        ("dist", None, "Clean distribution files"),
        ("api", None, "Clean generated API files"),
        ("docs", None, "Clean generated docs files"),
        ("all", None, "Clean all generated files"),
    ]

    def __init__(self, dist, **kw):
        super().__init__(dist, **kw)

        self.dist = None
        self.api = None
        self.docs = None
        self.all = None

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        paths = set()

        if self.dist:
            paths.update(Clean.DIST)

        if self.api:
            paths.update(Clean.API)

        if self.docs:
            paths.update(Clean.DOCS)

        if self.all or not paths:
            paths.update(Clean.ALL)

        for path in sorted(list(paths)):
            try:
                shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)
            except OSError:
                print("skipping {}".format(path))
            else:
                print("removing {}".format(path))


class Generate(Command):
    description = "Generate Pyrogram files"

    user_options = [
        ("api", None, "Generate API files"),
        ("docs", None, "Generate docs files")
    ]

    def __init__(self, dist, **kw):
        super().__init__(dist, **kw)

        self.api = None
        self.docs = None

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if self.api:
            errors_compiler.start()
            api_compiler.start()

        if self.docs:
            docs_compiler.start()


if len(argv) > 1 and argv[1] in ["bdist_wheel", "install", "develop"]:
    api_compiler.start()
    errors_compiler.start()

setup(
    name="Pyrogram",
    version=version,
    description="Elegant, modern and asynchronous Telegram MTProto API framework in Python for users and bots",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/pyrogram",
    download_url="https://github.com/pyrogram/pyrogram/releases/latest",
    author="Dan",
    author_email="dan@pyrogram.org",
    license="LGPLv3+",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet",
        "Topic :: Communications",
        "Topic :: Communications :: Chat",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries :: Application Frameworks"
    ],
    keywords="telegram chat messenger mtproto api client library python",
    project_urls={
        "Tracker": "https://github.com/pyrogram/pyrogram/issues",
        "Community": "https://t.me/pyrogram",
        "Source": "https://github.com/pyrogram/pyrogram",
        "Documentation": "https://docs.pyrogram.org",
    },
    python_requires="~=3.6",
    package_data = {
        "pyrogram": ["py.typed"],
    },
    packages=find_packages(exclude=["compiler*", "tests*"]),
    zip_safe=False,
    install_requires=requires,
    cmdclass={
        "clean": Clean,
        "generate": Generate
    }
)
