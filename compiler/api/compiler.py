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

import os
import re
import shutil

HOME = "compiler/api"
DESTINATION = "pyrogram/api"
notice_path = "NOTICE"
SECTION_RE = re.compile(r"---(\w+)---")
LAYER_RE = re.compile(r"//\sLAYER\s(\d+)")
COMBINATOR_RE = re.compile(r"^([\w.]+)#([0-9a-f]+)\s(?:.*)=\s([\w<>.]+);$", re.MULTILINE)
ARGS_RE = re.compile("[^{](\w+):([\w?!.<>]+)")
FLAGS_RE = re.compile(r"flags\.(\d+)\?")
FLAGS_RE_2 = re.compile(r"flags\.(\d+)\?([\w<>.]+)")

core_types = ["int", "long", "int128", "int256", "double", "bytes", "string", "Bool"]


class Combinator:
    def __init__(self, section: str, namespace: str, name: str, id: str, args: list, has_flags: bool, return_type: str):
        self.section = section
        self.namespace = namespace
        self.name = name
        self.id = id
        self.args = args
        self.has_flags = has_flags
        self.return_type = return_type


def snek(s: str):
    # https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
    s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", s)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s).lower()


def capit(s: str):
    return "".join([i[0].upper() + i[1:] for i in s.split("_")])


#
# def caml(s: str):
#     r = snek(s).split("_")
#     return "".join([str(i.title()) for i in r])


def sort_args(args):
    """Put flags at the end"""
    args = args.copy()
    flags = [i for i in args if FLAGS_RE.match(i[1])]

    for i in flags:
        args.remove(i)

    return args + flags


def start():
    shutil.rmtree("{}/types".format(DESTINATION), ignore_errors=True)
    shutil.rmtree("{}/functions".format(DESTINATION), ignore_errors=True)

    with open("{}/source/auth_key.tl".format(HOME)) as auth, \
            open("{}/source/sys_msgs.tl".format(HOME)) as system, \
            open("{}/source/main_api.tl".format(HOME)) as api:
        schema = (auth.read() + system.read() + api.read()).splitlines()

    with open("{}/template/class.txt".format(HOME)) as f:
        template = f.read()

    with open(notice_path) as f:
        notice = []

        for line in f.readlines():
            notice.append("# {}".format(line).strip())

        notice = "\n".join(notice)

    section = None
    layer = None
    namespaces = {"types": set(), "functions": set()}
    combinators = []

    for line in schema:
        # Check for section changer lines
        s = SECTION_RE.match(line)
        if s:
            section = s.group(1)
            continue

        # Save the layer version
        l = LAYER_RE.match(line)
        if l:
            layer = l.group(1)
            continue

        combinator = COMBINATOR_RE.match(line)
        if combinator:
            name, id, return_type = combinator.groups()
            namespace, name = name.split(".") if "." in name else ("", name)
            args = ARGS_RE.findall(line)

            # Check if combinator has flags
            for i in args:
                if FLAGS_RE.match(i[1]):
                    has_flags = True
                    break
            else:
                has_flags = False

            # Fix file and folder name collision
            if name == "updates":
                name = "update"

            # Fix arg name being "self" (reserved keyword)
            for i, item in enumerate(args):
                if item[0] == "self":
                    args[i] = ("is_self", item[1])

            if namespace:
                namespaces[section].add(namespace)

            combinators.append(
                Combinator(
                    section,
                    namespace,
                    name,
                    "0x{}".format(id.zfill(8)),
                    args,
                    has_flags,
                    return_type
                )
            )

    total = len(combinators)
    current = 0
    for c in combinators:  # type: Combinator
        print("Compiling APIs... [{}%] {}".format(
            str(round(current * 100 / total)).rjust(3),
            ".".join(filter(None, [c.section, c.namespace, c.name]))
        ), end="                \r", flush=True)
        current += 1

        path = "{}/{}/{}".format(DESTINATION, c.section, c.namespace)
        os.makedirs(path, exist_ok=True)

        init = "{}/__init__.py".format(path)

        if not os.path.exists(init):
            with open(init, "w") as f:
                f.write(notice + "\n\n")

        with open(init, "a") as f:
            f.write("from .{} import {}\n".format(snek(c.name), capit(c.name)))

        sorted_args = sort_args(c.args)

        arguments = ", " + ", ".join(
            ["{}{}".format(
                i[0],
                "=None" if FLAGS_RE.match(i[1]) else ""
            ) for i in sorted_args]
        ) if c.args else ""

        fields = "\n        ".join(
            ["self.{0} = {0}  # {1}".format(i[0], i[1]) for i in c.args]
        ) if c.args else "pass"

        docstring_args = []

        for i, arg in enumerate(sorted_args):
            arg_name, arg_type = arg
            is_optional = arg_type.startswith("flags.")
            arg_type = arg_type.split("?")[-1]

            if arg_type in core_types:
                if "int" in arg_type or arg_type == "long":
                    arg_type = ":obj:`int`"
                elif arg_type == "double":
                    arg_type = ":obj:`float`"
                else:
                    arg_type = ":obj:`{}`".format(arg_type.lower())
            elif arg_type == "true":
                arg_type = ":obj:`bool`"
            else:
                if arg_type.startswith("Vector"):
                    sub_type = arg_type.split("<")[1][:-1]

                    if sub_type in core_types:
                        if "int" in sub_type or sub_type == "long":
                            arg_type = "List of :obj:`int`"
                        elif sub_type == "double":
                            arg_type = "List of :obj:`float`"
                        else:
                            arg_type = "List of :obj:`{}`".format(sub_type.lower())
                    else:
                        arg_type = "List of :class:`pyrogram.api.types.{}`".format(
                            ".".join(
                                sub_type.split(".")[:-1]
                                + [capit(sub_type.split(".")[-1])]
                            )
                        )
                else:
                    arg_type = ":class:`pyrogram.api.types.{}`".format(
                        ".".join(
                            arg_type.split(".")[:-1]
                            + [capit(arg_type.split(".")[-1])]
                        )
                    )

            docstring_args.append(
                "{}: {}{}".format(
                    arg_name,
                    arg_type,
                    " (optional)" if is_optional else ""
                )
            )

        if docstring_args:
            docstring_args = "Args:\n        " + "\n        ".join(docstring_args)
        else:
            docstring_args = "No parameters required."

        docstring_args = "Attributes:\n        ID (:obj:`int`): ``{}``\n\n    ".format(c.id) + docstring_args

        docstring_args += "\n\n    Returns:\n        "
        if c.return_type in core_types:
            if "int" in c.return_type or c.return_type == "long":
                return_type = ":obj:`int`"
            elif c.return_type == "double":
                return_type = ":obj:`float`"
            else:
                return_type = ":obj:`{}`".format(c.return_type.lower())
        else:
            if c.return_type.startswith("Vector"):
                sub_type = c.return_type.split("<")[1][:-1]

                if sub_type in core_types:
                    if "int" in sub_type or sub_type == "long":
                        return_type = "List of :obj:`int`"
                    elif sub_type == "double":
                        return_type = "List of :obj:`float`"
                    else:
                        return_type = "List of :obj:`{}`".format(c.return_type.lower())
                else:
                    return_type = "List of :class:`pyrogram.api.types.{}`".format(
                        ".".join(
                            sub_type.split(".")[:-1]
                            + [capit(sub_type.split(".")[-1])]
                        )
                    )
            else:
                return_type = ":class:`pyrogram.api.types.{}`".format(
                    ".".join(
                        c.return_type.split(".")[:-1]
                        + [capit(c.return_type.split(".")[-1])]
                    )
                )

        docstring_args += return_type

        if c.section == "functions":
            docstring_args += "\n\n    Raises:\n        :class:`pyrogram.Error`"

        if c.has_flags:
            write_flags = []
            for i in c.args:
                flag = FLAGS_RE.match(i[1])
                if flag:
                    write_flags.append("flags |= (1 << {}) if self.{} is not None else 0".format(flag.group(1), i[0]))

            write_flags = "\n        ".join([
                "flags = 0",
                "\n        ".join(write_flags),
                "b.write(Int(flags))"
            ])
        else:
            write_flags = "# No flags"

        read_flags = "flags = Int.read(b)" if c.has_flags else "# No flags"

        write_types = read_types = ""

        for arg_name, arg_type in c.args:
            flag = FLAGS_RE_2.findall(arg_type)

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

        with open("{}/{}.py".format(path, snek(c.name)), "w") as f:
            f.write(
                template.format(
                    notice=notice,
                    class_name=capit(c.name),
                    docstring_args=docstring_args,
                    object_id=c.id,
                    arguments=arguments,
                    fields=fields,
                    read_flags=read_flags,
                    read_types=read_types,
                    write_flags=write_flags,
                    write_types=write_types,
                    return_arguments=", ".join([i[0] for i in sorted_args])
                )
            )

    with open("{}/all.py".format(DESTINATION), "w") as f:
        f.write(notice + "\n\n")
        f.write("layer = {}\n\n".format(layer))
        f.write("objects = {")

        for c in combinators:
            path = ".".join(filter(None, [c.section, c.namespace, capit(c.name)]))
            f.write("\n    {}: \"{}\",".format(c.id, path))

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

    for k, v in namespaces.items():
        with open("{}/{}/__init__.py".format(DESTINATION, k), "a") as f:
            f.write("from . import {}\n".format(", ".join([i for i in v])) if v else "")


if "__main__" == __name__:
    HOME = "."
    DESTINATION = "../../pyrogram/api"
    notice_path = "../../NOTICE"
    start()
