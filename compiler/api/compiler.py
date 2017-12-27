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

import os
import re
import shutil

home = "compiler/api"
dest = "pyrogram/api"
notice_path = "NOTICE"

core_types = ["int", "long", "int128", "int256", "double", "bytes", "string", "Bool"]


# TODO: Compiler was written in a rush. variables/methods name and pretty much all the code is fuzzy, but it works
# TODO: Some constructors have flags:# but not flags.\d+\?

class Compiler:
    def __init__(self):
        self.section = "types"  # TL Schema starts with types
        self.namespaces = {"types": set(), "functions": set()}
        self.objects = {}
        self.layer = None

        self.schema = None

        with open("{}/template/class.txt".format(home)) as f:
            self.template = f.read()

        with open(notice_path) as f:
            notice = []

            for line in f.readlines():
                notice.append("# {}".format(line).strip())

            self.notice = "\n".join(notice)

    def read_schema(self):
        """Read schema files"""
        with open("{}/source/auth_key.tl".format(home)) as auth, \
                open("{}/source/sys_msgs.tl".format(home)) as system, \
                open("{}/source/main_api.tl".format(home)) as api:
            self.schema = auth.read() + system.read() + api.read()

    def parse_schema(self):
        """Parse schema line by line"""
        total = len(self.schema.splitlines())

        for i, line in enumerate(self.schema.splitlines()):
            # Check for section changer lines
            section = re.match(r"---(\w+)---", line)
            if section:
                self.section = section.group(1)
                continue

            # Save the layer version
            layer = re.match(r"//\sLAYER\s(\d+)", line)
            if layer:
                self.layer = layer.group(1)
                continue

            combinator = re.match(r"^([\w.]+)#([0-9a-f]+)\s(.*)=\s([\w<>.]+);$", line, re.MULTILINE)

            if combinator:
                name, id, args, type = combinator.groups()
                namespace, name = name.split(".") if "." in name else ("", name)
                args = re.findall(r"[^{](\w+):([\w?!.<>]+)", line)

                print("Compiling APIs: [{}%]".format(round(i * 100 / total)), end="\r")

                for i in args:
                    if re.match(r"flags\.\d+\?", i[1]):
                        has_flags = True
                        break
                else:
                    has_flags = False

                if name == "updates":
                    name = "update"

                for i, item in enumerate(args):
                    # if item[0] in keyword.kwlist + dir(builtins) + ["self"]:
                    if item[0] == "self":
                        args[i] = ("is_{}".format(item[0]), item[1])

                if namespace:
                    self.namespaces[self.section].add(namespace)

                self.compile(namespace, name, id, args, has_flags)

                self.objects[id] = "{}.{}{}.{}".format(
                    self.section,
                    "{}.".format(namespace) if namespace else "",
                    self.snek(name),
                    self.caml(name)
                )

    def finish(self):
        with open("{}/all.py".format(dest), "w") as f:
            f.write(self.notice + "\n\n")
            f.write("layer = {}\n\n".format(self.layer))
            f.write("objects = {")

            for k, v in self.objects.items():
                v = v.split(".")
                del v[-2]
                v = ".".join(v)

                f.write("\n    0x{}: \"{}\",".format(k.zfill(8), v))

            f.write("\n    0xbc799737: \"core.BoolFalse\",")
            f.write("\n    0x997275b5: \"core.BoolTrue\",")
            f.write("\n    0x56730bcc: \"core.Null\",")
            f.write("\n    0x1cb5c415: \"core.Vector\",")
            f.write("\n    0x73f1f8dc: \"core.MsgContainer\",")
            f.write("\n    0xae500895: \"core.FutureSalts\",")
            f.write("\n    0x0949d9dc: \"core.FutureSalt\",")
            f.write("\n    0x3072cfa1: \"core.GzipPacked\",")
            f.write("\n    0x5bb8e511: \"core.Message\"")

            f.write("\n}\n")

        for k, v in self.namespaces.items():
            with open("{}/{}/__init__.py".format(dest, k), "a") as f:
                f.write("from . import {}\n".format(", ".join([i for i in v])) if v else "")

    @staticmethod
    def sort_args(args):
        """Put flags at the end"""
        args = args.copy()
        flags = [i for i in args if re.match(r"flags\.\d+\?", i[1])]

        for i in flags:
            args.remove(i)

        return args + flags

    def compile(self, namespace, name, id, args, has_flags):
        path = "{}/{}/{}".format(dest, self.section, namespace)
        os.makedirs(path, exist_ok=True)

        init = "{}/__init__.py".format(path)

        if not os.path.exists(init):
            with open(init, "w") as f:
                f.write(self.notice + "\n\n")

        with open(init, "a") as f:
            f.write("from .{} import {}\n".format(self.snek(name), self.caml(name)))

        sorted_args = self.sort_args(args)

        object_id = "0x{}".format(id)

        arguments = ", " + ", ".join(
            ["{}{}".format(
                i[0],
                "=None" if re.match(r"flags\.\d+\?", i[1]) else ""
            ) for i in sorted_args]
        ) if args else ""

        fields = "\n        ".join(
            ["self.{0} = {0}  # {1}".format(i[0], i[1]) for i in args]
        ) if args else "pass"

        if has_flags:
            write_flags = []
            for i in args:
                flag = re.match(r"flags\.(\d+)\?", i[1])
                if flag:
                    write_flags.append("flags |= (1 << {}) if self.{} is not None else 0".format(flag.group(1), i[0]))

            write_flags = "\n        ".join([
                "flags = 0",
                "\n        ".join(write_flags),
                "b.write(Int(flags))"
            ])
        else:
            write_flags = "# No flags"

        read_flags = "flags = Int.read(b)" if has_flags else "# No flags"

        write_types = read_types = ""

        for arg_name, arg_type in args:
            flag = re.findall(r"flags\.(\d+)\?([\w<>.]+)", arg_type)

            if flag:
                index, flag_type = flag[0]

                if flag_type == "true":
                    read_types += "\n        "
                    read_types += "{} = True if flags & (1 << {}) else False".format(arg_name, index)
                elif flag_type in core_types:
                    write_types += "\n        "
                    write_types += "if self.{} is not None:\n            ".format(arg_name)
                    write_types += "b.write({}(self.{}))\n        ".format(flag_type.title(), arg_name)

                    read_types += "\n        "
                    read_types += "{} = {}.read(b) if flags & (1 << {}) else None".format(
                        arg_name, flag_type.title(), index
                    )
                elif "vector" in flag_type.lower():
                    sub_type = arg_type.split("<")[1][:-1]

                    write_types += "\n        "
                    write_types += "if self.{} is not None:\n            ".format(arg_name)
                    write_types += "b.write(Vector(self.{}{}))\n        ".format(
                        arg_name, ", {}".format(sub_type.title()) if sub_type in core_types else ""
                    )

                    read_types += "\n        "
                    read_types += "{} = Object.read(b{}) if flags & (1 << {}) else []\n        ".format(
                        arg_name, ", {}".format(sub_type.title()) if sub_type in core_types else "", index
                    )
                else:
                    write_types += "\n        "
                    write_types += "if self.{} is not None:\n            ".format(arg_name)
                    write_types += "b.write(self.{}.write())\n        ".format(arg_name)

                    read_types += "\n        "
                    read_types += "{} = Object.read(b) if flags & (1 << {}) else None\n        ".format(
                        arg_name, index
                    )
            else:
                if arg_type in core_types:
                    write_types += "\n        "
                    write_types += "b.write({}(self.{}))\n        ".format(arg_type.title(), arg_name)

                    read_types += "\n        "
                    read_types += "{} = {}.read(b)\n        ".format(arg_name, arg_type.title())
                elif "vector" in arg_type.lower():
                    sub_type = arg_type.split("<")[1][:-1]

                    write_types += "\n        "
                    write_types += "b.write(Vector(self.{}{}))\n        ".format(
                        arg_name, ", {}".format(sub_type.title()) if sub_type in core_types else ""
                    )

                    read_types += "\n        "
                    read_types += "{} = Object.read(b{})\n        ".format(
                        arg_name, ", {}".format(sub_type.title()) if sub_type in core_types else ""
                    )
                else:
                    write_types += "\n        "
                    write_types += "b.write(self.{}.write())\n        ".format(arg_name)

                    read_types += "\n        "
                    read_types += "{} = Object.read(b)\n        ".format(arg_name)

        with open("{}/{}.py".format(path, self.snek(name)), "w") as f:
            f.write(
                self.template.format(
                    notice=self.notice,
                    class_name=self.caml(name),
                    object_id=object_id,
                    arguments=arguments,
                    fields=fields,
                    read_flags=read_flags,
                    read_types=read_types,
                    write_flags=write_flags,
                    write_types=write_types,
                    return_arguments=", ".join([i[0] for i in sorted_args])
                )
            )

    @staticmethod
    def snek(s):
        # https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
        s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", s)
        return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s).lower()

    @staticmethod
    def caml(s):
        s = Compiler.snek(s).split("_")
        return "".join([str(i.title()) for i in s])

    def start(self):
        shutil.rmtree("{}/types".format(dest), ignore_errors=True)
        shutil.rmtree("{}/functions".format(dest), ignore_errors=True)

        self.read_schema()
        self.parse_schema()
        self.finish()

        print()


def start():
    c = Compiler()
    c.start()


if "__main__" == __name__:
    home = "."
    dest = "../../pyrogram/api"
    notice_path = "../../NOTICE"

    start()
