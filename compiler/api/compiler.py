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
NOTICE_PATH = "NOTICE"
SECTION_RE = re.compile(r"---(\w+)---")
LAYER_RE = re.compile(r"//\sLAYER\s(\d+)")
COMBINATOR_RE = re.compile(r"^([\w.]+)#([0-9a-f]+)\s(?:.*)=\s([\w<>.]+);(?: // Docs: (.+))?$", re.MULTILINE)
ARGS_RE = re.compile("[^{](\w+):([\w?!.<>]+)")
FLAGS_RE = re.compile(r"flags\.(\d+)\?")
FLAGS_RE_2 = re.compile(r"flags\.(\d+)\?([\w<>.]+)")
FLAGS_RE_3 = re.compile(r"flags:#")
INT_RE = re.compile(r"int(\d+)")

core_types = ["int", "long", "int128", "int256", "double", "bytes", "string", "Bool"]
types_to_constructors = {}
types_to_functions = {}
constructors_to_functions = {}


def get_docstring_arg_type(t: str, is_list: bool = False, is_pyrogram_type: bool = False):
    if t in core_types:
        if t == "long":
            return "``int`` ``64-bit``"
        elif "int" in t:
            size = INT_RE.match(t)
            return "``int`` ``{}-bit``".format(size.group(1)) if size else "``int`` ``32-bit``"
        elif t == "double":
            return "``float`` ``64-bit``"
        elif t == "string":
            return "``str``"
        else:
            return "``{}``".format(t.lower())
    elif t == "true":
        return "``bool``"
    elif t == "Object" or t == "X":
        return "Any object from :obj:`pyrogram.api.types`"
    elif t == "!X":
        return "Any method from :obj:`pyrogram.api.functions`"
    elif t.startswith("Vector"):
        return "List of " + get_docstring_arg_type(t.split("<", 1)[1][:-1], True, is_pyrogram_type)
    else:
        if is_pyrogram_type:
            t = "pyrogram." + t

        t = types_to_constructors.get(t, [t])
        n = len(t) - 1

        t = (("e" if is_list else "E") + "ither " if n else "") + ", ".join(
            ":obj:`{1} <{0}.{1}>`".format(
                "pyrogram.types" if is_pyrogram_type else "pyrogram.api.types",
                i.replace("pyrogram.", "")
            )
            for i in t
        )

        if n:
            t = t.split(", ")
            t = ", ".join(t[:-1]) + " or " + t[-1]

        return t


def get_references(t: str):
    t = constructors_to_functions.get(t)

    if t:
        n = len(t) - 1

        t = ", ".join(
            ":obj:`{0} <pyrogram.api.functions.{0}>`".format(i)
            for i in t
        )

        if n:
            t = t.split(", ")
            t = ", ".join(t[:-1]) + " and " + t[-1]

    return t


def get_argument_type(arg):
    is_flag = FLAGS_RE.match(arg[1])
    name, t = arg

    if is_flag:
        t = t.split("?")[1]

    if t in core_types:
        if t == "long" or "int" in t:
            t = ": int"
        elif t == "double":
            t = ": float"
        elif t == "string":
            t = ": str"
        else:
            t = ": {}".format(t.lower())
    elif t == "true":
        t = ": bool"
    elif t.startswith("Vector"):
        t = ": list"
    else:
        return name + ("=None" if is_flag else "")

    return name + t + (" = None" if is_flag else "")


class Combinator:
    def __init__(self,
                 section: str,
                 namespace: str,
                 name: str,
                 id: str,
                 args: list,
                 has_flags: bool,
                 return_type: str,
                 docs: str):
        self.section = section
        self.namespace = namespace
        self.name = name
        self.id = id
        self.args = args
        self.has_flags = has_flags
        self.return_type = return_type
        self.docs = docs


def snek(s: str):
    # https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
    s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", s)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s).lower()


def capit(s: str):
    return "".join([i[0].upper() + i[1:] for i in s.split("_")])


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

    with open("{}/source/auth_key.tl".format(HOME), encoding="utf-8") as auth, \
            open("{}/source/sys_msgs.tl".format(HOME), encoding="utf-8") as system, \
            open("{}/source/main_api.tl".format(HOME), encoding="utf-8") as api, \
            open("{}/source/pyrogram.tl".format(HOME), encoding="utf-8") as pyrogram:
        schema = (auth.read() + system.read() + api.read() + pyrogram.read()).splitlines()

    with open("{}/template/mtproto.txt".format(HOME), encoding="utf-8") as f:
        mtproto_template = f.read()

    with open("{}/template/pyrogram.txt".format(HOME), encoding="utf-8") as f:
        pyrogram_template = f.read()

    with open(NOTICE_PATH, encoding="utf-8") as f:
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
            name, id, return_type, docs = combinator.groups()
            namespace, name = name.split(".") if "." in name else ("", name)
            args = ARGS_RE.findall(line.split(" //")[0])

            # Pingu!
            has_flags = not not FLAGS_RE_3.findall(line)

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
                    capit(name),
                    "0x{}".format(id.zfill(8)),
                    args,
                    has_flags,
                    ".".join(
                        return_type.split(".")[:-1]
                        + [capit(return_type.split(".")[-1])]
                    ),
                    docs
                )
            )

    for c in combinators:
        return_type = c.return_type

        if return_type.startswith("Vector"):
            return_type = return_type.split("<")[1][:-1]

        d = types_to_constructors if c.section == "types" else types_to_functions

        if return_type not in d:
            d[return_type] = []

        d[return_type].append(".".join(filter(None, [c.namespace, c.name])))

    for k, v in types_to_constructors.items():
        for i in v:
            try:
                constructors_to_functions[i] = types_to_functions[k]
            except KeyError:
                pass

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
            with open(init, "w", encoding="utf-8") as f:
                f.write(notice + "\n\n")

        with open(init, "a", encoding="utf-8") as f:
            f.write("from .{} import {}\n".format(snek(c.name), capit(c.name)))

        sorted_args = sort_args(c.args)

        arguments = ", " + ", ".join(
            [get_argument_type(i) for i in sorted_args]
        ) if c.args else ""

        fields = "\n        ".join(
            ["self.{0} = {0}  # {1}".format(i[0], i[1]) for i in c.args]
        ) if c.args else "pass"

        docstring_args = []
        docs = c.docs.split("|")[1:] if c.docs else None

        for i, arg in enumerate(sorted_args):
            arg_name, arg_type = arg
            is_optional = FLAGS_RE.match(arg_type)
            flag_number = is_optional.group(1) if is_optional else -1
            arg_type = arg_type.split("?")[-1]

            if docs:
                docstring_args.append(
                    "{} ({}{}):\n            {}\n".format(
                        arg_name,
                        get_docstring_arg_type(arg_type, is_pyrogram_type=True),
                        ", optional" if "Optional" in docs[i] else "",
                        re.sub("Optional\. ", "", docs[i].split("§")[1].rstrip(".") + ".")
                    )
                )
            else:
                docstring_args.append(
                    "{}{}: {}".format(
                        arg_name,
                        " (optional)".format(flag_number) if is_optional else "",
                        get_docstring_arg_type(arg_type, is_pyrogram_type=c.namespace == "pyrogram")
                    )
                )

        if docstring_args:
            docstring_args = "Args:\n        " + "\n        ".join(docstring_args)
        else:
            docstring_args = "No parameters required."

        docstring_args = "Attributes:\n        ID: ``{}``\n\n    ".format(c.id) + docstring_args

        if c.section == "functions":
            docstring_args += "\n\n    Raises:\n        :obj:`Error <pyrogram.Error>`"
            docstring_args += "\n\n    Returns:\n        " + get_docstring_arg_type(c.return_type)
        else:
            references = get_references(".".join(filter(None, [c.namespace, c.name])))

            if references:
                docstring_args += "\n\n    See Also:\n        This object can be returned by " + references + "."

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

        if c.docs:
            description = c.docs.split("|")[0].split("§")[1]
            docstring_args = description + "\n\n    " + docstring_args

        with open("{}/{}.py".format(path, snek(c.name)), "w", encoding="utf-8") as f:
            if c.docs:
                f.write(
                    pyrogram_template.format(
                        notice=notice,
                        class_name=capit(c.name),
                        docstring_args=docstring_args,
                        object_id=c.id,
                        arguments=arguments,
                        fields=fields
                    )
                )
            else:
                f.write(
                    mtproto_template.format(
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

    with open("{}/all.py".format(DESTINATION), "w", encoding="utf-8") as f:
        f.write(notice + "\n\n")
        f.write("layer = {}\n\n".format(layer))
        f.write("objects = {")

        for c in combinators:
            path = ".".join(filter(None, [c.section, c.namespace, capit(c.name)]))
            f.write("\n    {}: \"pyrogram.api.{}\",".format(c.id, path))

        f.write("\n    0xbc799737: \"pyrogram.api.core.BoolFalse\",")
        f.write("\n    0x997275b5: \"pyrogram.api.core.BoolTrue\",")
        f.write("\n    0x56730bcc: \"pyrogram.api.core.Null\",")
        f.write("\n    0x1cb5c415: \"pyrogram.api.core.Vector\",")
        f.write("\n    0x73f1f8dc: \"pyrogram.api.core.MsgContainer\",")
        f.write("\n    0xae500895: \"pyrogram.api.core.FutureSalts\",")
        f.write("\n    0x0949d9dc: \"pyrogram.api.core.FutureSalt\",")
        f.write("\n    0x3072cfa1: \"pyrogram.api.core.GzipPacked\",")
        f.write("\n    0x5bb8e511: \"pyrogram.api.core.Message\",")

        f.write("\n    0xb0700000: \"pyrogram.client.types.Update\",")
        f.write("\n    0xb0700001: \"pyrogram.client.types.User\",")
        f.write("\n    0xb0700002: \"pyrogram.client.types.Chat\",")
        f.write("\n    0xb0700003: \"pyrogram.client.types.Message\",")
        f.write("\n    0xb0700004: \"pyrogram.client.types.MessageEntity\",")
        f.write("\n    0xb0700005: \"pyrogram.client.types.PhotoSize\",")
        f.write("\n    0xb0700006: \"pyrogram.client.types.Audio\",")
        f.write("\n    0xb0700007: \"pyrogram.client.types.Document\",")
        f.write("\n    0xb0700008: \"pyrogram.client.types.Video\",")
        f.write("\n    0xb0700009: \"pyrogram.client.types.Voice\",")
        f.write("\n    0xb0700010: \"pyrogram.client.types.VideoNote\",")
        f.write("\n    0xb0700011: \"pyrogram.client.types.Contact\",")
        f.write("\n    0xb0700012: \"pyrogram.client.types.Location\",")
        f.write("\n    0xb0700013: \"pyrogram.client.types.Venue\",")
        f.write("\n    0xb0700014: \"pyrogram.client.types.UserProfilePhotos\",")
        f.write("\n    0xb0700015: \"pyrogram.client.types.ChatPhoto\",")
        f.write("\n    0xb0700016: \"pyrogram.client.types.ChatMember\",")
        f.write("\n    0xb0700017: \"pyrogram.client.types.Sticker\",")
        f.write("\n    0xb0700018: \"pyrogram.client.types.reply_markup.ForceReply\",")
        f.write("\n    0xb0700019: \"pyrogram.client.types.reply_markup.InlineKeyboardButton\",")
        f.write("\n    0xb0700020: \"pyrogram.client.types.reply_markup.InlineKeyboardMarkup\",")
        f.write("\n    0xb0700021: \"pyrogram.client.types.reply_markup.KeyboardButton\",")
        f.write("\n    0xb0700022: \"pyrogram.client.types.reply_markup.ReplyKeyboardMarkup\",")
        f.write("\n    0xb0700023: \"pyrogram.client.types.reply_markup.ReplyKeyboardRemove\",")
        f.write("\n    0xb0700024: \"pyrogram.client.types.CallbackQuery\",")
        f.write("\n    0xb0700025: \"pyrogram.client.types.GIF\",")
        f.write("\n    0xb0700026: \"pyrogram.client.types.Messages\",")
        f.write("\n    0xb0700027: \"pyrogram.client.types.Photo\",")
        f.write("\n    0xb0700028: \"pyrogram.client.types.Dialog\",")
        f.write("\n    0xb0700029: \"pyrogram.client.types.Dialogs\",")

        f.write("\n}\n")

    for k, v in namespaces.items():
        with open("{}/{}/__init__.py".format(DESTINATION, k), "a", encoding="utf-8") as f:
            f.write("from . import {}\n".format(", ".join([i for i in v])) if v else "")


if "__main__" == __name__:
    HOME = "."
    DESTINATION = "../../pyrogram/api"
    NOTICE_PATH = "../../NOTICE"
    start()
