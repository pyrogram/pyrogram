# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017 Dan Tès <https://github.com/delivrance>
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

import csv
import os
import re
import shutil

home = "compiler/error"
dest = "pyrogram/api/errors/exceptions"
notice_path = "NOTICE"


def snek(s):
    # https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
    s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", s)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s).lower()


def caml(s):
    s = snek(s).split("_")
    return "".join([str(i.title()) for i in s])


def start():
    shutil.rmtree(dest, ignore_errors=True)
    os.makedirs(dest)

    files = [i for i in os.listdir("{}/source".format(home))]

    with open(notice_path) as f:
        notice = []

        for line in f.readlines():
            notice.append("# {}".format(line).strip())

        notice = "\n".join(notice)

    with open("{}/all.py".format(dest), "w") as f_all:
        f_all.write(notice + "\n\n")
        f_all.write("count = {count}\n\n")
        f_all.write("exceptions = {\n")

        count = 0

        for i in files:
            code, name = re.search(r"(\d+)_([A-Z_]+)", i).groups()

            f_all.write("    {}: {{\n".format(code))

            init = "{}/__init__.py".format(dest)

            if not os.path.exists(init):
                with open(init, "w") as f_init:
                    f_init.write(notice + "\n\n")

            with open(init, "a") as f_init:
                f_init.write("from .{}_{} import *\n".format(name.lower(), code))

            with open("{}/source/{}".format(home, i)) as f_csv, \
                    open("{}/{}_{}.py".format(dest, name.lower(), code), "w") as f_class:
                reader = csv.reader(f_csv, delimiter="\t")

                super_class = caml(name)
                name = " ".join([str(i.capitalize()) for i in re.sub(r"_", " ", name).lower().split(" ")])

                sub_classes = []

                for j, row in enumerate(reader):
                    if j == 0:
                        continue

                    count += 1

                    if not row:  # Row is empty (blank line)
                        continue

                    id, message = row

                    sub_class = caml(re.sub(r"_X", "_", id))

                    f_all.write("        \"{}\": \"{}\",\n".format(id, sub_class))

                    sub_classes.append((sub_class, id, message))

                with open("{}/template/class.txt".format(home), "r") as f_class_template:
                    class_template = f_class_template.read()

                    with open("{}/template/sub_class.txt".format(home), "r") as f_sub_class_template:
                        sub_class_template = f_sub_class_template.read()

                    class_template = class_template.format(
                        notice=notice,
                        super_class=super_class,
                        code=code,
                        name="\"{}\"".format(name),
                        sub_classes="".join([sub_class_template.format(
                            sub_class=k[0],
                            super_class=super_class,
                            id="\"{}\"".format(k[1]),
                            message="\"{}\"".format(k[2])
                        ) for k in sub_classes])
                    )

                f_class.write(class_template)

            f_all.write("    },\n")

        f_all.write("}\n")

    with open("{}/all.py".format(dest)) as f:
        content = f.read()

    with open("{}/all.py".format(dest), "w") as f:
        f.write(re.sub("{count}", str(count), content))

    print("Compiling Errors: [100%]")


if "__main__" == __name__:
    home = "."
    dest = "../../pyrogram/api/errors/exceptions"
    notice_path = "../../NOTICE"

    start()
