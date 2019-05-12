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

import ast
import os
import shutil

HOME = "compiler/docs"
DESTINATION = "docs/source/telegram"

FUNCTIONS_PATH = "pyrogram/api/functions"
TYPES_PATH = "pyrogram/api/types"

FUNCTIONS_BASE = "functions"
TYPES_BASE = "types"

shutil.rmtree(TYPES_BASE, ignore_errors=True)
shutil.rmtree(FUNCTIONS_BASE, ignore_errors=True)


def generate(source_path, base):
    all_entities = {}

    def build(path, level=0):
        last = path.split("/")[-1]

        for i in os.listdir(path):
            try:
                if not i.startswith("__"):
                    build("/".join([path, i]), level=level + 1)
            except NotADirectoryError:
                with open(path + "/" + i, encoding="utf-8") as f:
                    p = ast.parse(f.read())

                for node in ast.walk(p):
                    if isinstance(node, ast.ClassDef):
                        name = node.name

                # name = "".join([str(j.title()) for j in os.path.splitext(i)[0].split("_")])
                full_path = os.path.basename(path) + "/" + name + ".rst"

                if level:
                    full_path = base + "/" + full_path

                os.makedirs(os.path.dirname(DESTINATION + "/" + full_path), exist_ok=True)

                with open(DESTINATION + "/" + full_path, "w", encoding="utf-8") as f:
                    f.write(
                        page_template.format(
                            title=name,
                            title_markup="=" * len(name),
                            full_class_path="pyrogram.api.{}".format(
                                os.path.splitext(full_path)[0].replace("/", ".")
                            )
                        )
                    )

                if last not in all_entities:
                    all_entities[last] = []

                all_entities[last].append(name)

    build(source_path)

    for k, v in sorted(all_entities.items()):
        v = sorted(v)
        entities = []

        for i in v:
            entities.append(i)

        if k != base:
            inner_path = base + "/" + k + "/index" + ".rst"
            module = "pyrogram.api.{}.{}".format(base, k)
        else:
            for i in sorted(list(all_entities), reverse=True):
                if i != base:
                    entities.insert(0, "{0}/index".format(i))

            inner_path = base + "/index" + ".rst"
            module = "pyrogram.api.{}".format(base)

        with open(DESTINATION + "/" + inner_path, "w", encoding="utf-8") as f:
            if k == base:
                f.write(":tocdepth: 1\n\n")

            f.write(
                toctree.format(
                    title=k.title(),
                    title_markup="=" * len(k),
                    module=module,
                    entities="\n    ".join(entities)
                )
            )

            f.write("\n")


def start():
    global page_template
    global toctree

    with open(HOME + "/template/page.txt", encoding="utf-8") as f:
        page_template = f.read()

    with open(HOME + "/template/toctree.txt", encoding="utf-8") as f:
        toctree = f.read()

    generate(TYPES_PATH, TYPES_BASE)
    generate(FUNCTIONS_PATH, FUNCTIONS_BASE)


if "__main__" == __name__:
    FUNCTIONS_PATH = "../../pyrogram/api/functions"
    TYPES_PATH = "../../pyrogram/api/types"
    HOME = "."
    DESTINATION = "../../docs/source/telegram"

    start()
