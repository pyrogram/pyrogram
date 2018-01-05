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
import ast
import os
import shutil

home = "compiler/docs"
destination = "docs/source"

functions_path = "pyrogram/api/functions"
types_path = "pyrogram/api/types"

functions_base = "functions"
types_base = "types"

shutil.rmtree(types_base, ignore_errors=True)
shutil.rmtree(functions_base, ignore_errors=True)

with open(home + "/template/page.txt") as f:
    page_template = f.read()

with open(home + "/template/toctree.txt") as f:
    toctree = f.read()


def generate(source_path, base):
    all_entities = {}

    def build(path, level=0):
        last = path.split("/")[-1]

        for i in os.listdir(path):
            try:
                if not i.startswith("__"):
                    build("/".join([path, i]), level=level + 1)
            except NotADirectoryError:
                with open(path + "/" + i) as f:
                    p = ast.parse(f.read())

                for node in ast.walk(p):
                    if isinstance(node, ast.ClassDef):
                        name = node.name

                # name = "".join([str(j.title()) for j in os.path.splitext(i)[0].split("_")])
                full_path = os.path.basename(path) + "/" + name + ".rst"

                if level:
                    full_path = base + "/" + full_path

                os.makedirs(os.path.dirname(destination + "/" + full_path), exist_ok=True)

                with open(destination + "/" + full_path, "w") as f:
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

    for k, v in all_entities.items():
        entities = []

        for i in v:
            entities.append(i)

        if k != base:
            inner_path = base + "/" + k + "/index" + ".rst"
        else:
            for i in list(all_entities)[::-1]:
                if i != base:
                    entities.insert(0, "{0}/index".format(i))

            inner_path = base + "/index" + ".rst"

        with open(destination + "/" + inner_path, "w") as f:
            f.write(
                toctree.format(
                    title=k.title(),
                    title_markup="=" * len(k),
                    entities="\n    ".join(entities)
                )
            )

            f.write("\n")


def start():
    generate(types_path, types_base)
    generate(functions_path, functions_base)


if "__main__" == __name__:
    functions_path = "../../pyrogram/api/functions"
    types_path = "../../pyrogram/api/types"
    home = "."
    destination = "../../docs/source"

    start()
