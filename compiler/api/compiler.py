#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2020 Dan <https://github.com/delivrance>
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
from pathlib import Path
from typing import NamedTuple, List, Tuple

HOME_PATH = Path("compiler/api")
DESTINATION_PATH = Path("pyrogram/api")
NOTICE_PATH = "NOTICE"

SECTION_RE = re.compile(r"---(\w+)---")
LAYER_RE = re.compile(r"//\sLAYER\s(\d+)")
COMBINATOR_RE = re.compile(r"^([\w.]+)#([0-9a-f]+)\s(?:.*)=\s([\w<>.]+);$", re.MULTILINE)
ARGS_RE = re.compile(r"[^{](\w+):([\w?!.<>#]+)")
FLAGS_RE = re.compile(r"flags\.(\d+)\?")
FLAGS_RE_2 = re.compile(r"flags\.(\d+)\?([\w<>.]+)")
FLAGS_RE_3 = re.compile(r"flags:#")
INT_RE = re.compile(r"int(\d+)")

CORE_TYPES = ["int", "long", "int128", "int256", "double", "bytes", "string", "Bool", "true"]


class Combinator(NamedTuple):
    section: str
    name: str
    id: str
    has_flags: bool
    args: List[Tuple[str, str]]
    type: str


def snake(s: str):
    # https://stackoverflow.com/q/1175208
    s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", s)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s).lower()


def camel(s: str):
    return "".join([i[0].upper() + i[1:] for i in s.split("_")])


# noinspection PyShadowingBuiltins, PyShadowingNames
def get_type_hint(type: str) -> str:
    is_flag = FLAGS_RE.match(type)
    is_core = False

    if is_flag:
        type = type.split("?")[1]

    if type in CORE_TYPES:
        is_core = True

        if type == "long" or "int" in type:
            type = "int"
        elif type == "double":
            type = "float"
        elif type == "string":
            type = "str"
        elif type in ["Bool", "true"]:
            type = "bool"
        else:  # bytes and object
            type = "bytes"

    if type == "Object":
        return "object"

    if re.match("^vector", type, re.I):
        is_core = True

        sub_type = type.split("<")[1][:-1]
        type = f"List[{get_type_hint(sub_type)}]"

    if is_core:
        return f'{type}{" = None" if is_flag else ""}'
    else:
        ns, name = type.split(".") if "." in type else ("", type)
        name = f"T{name}"
        type = ".".join([ns, name]).strip(".")

        return f'"types.{type}"{" = None" if is_flag else ""}'


def sort_args(args):
    """Put flags at the end"""
    args = args.copy()
    flags = [i for i in args if FLAGS_RE.match(i[1])]

    for i in flags:
        args.remove(i)

    try:
        args.remove(("flags", "#"))
    except ValueError:
        pass

    return args + flags


# noinspection PyShadowingBuiltins
def start():
    shutil.rmtree(DESTINATION_PATH / "types", ignore_errors=True)
    shutil.rmtree(DESTINATION_PATH / "functions", ignore_errors=True)

    with open("source/auth_key.tl") as f1, open("source/sys_msgs.tl") as f2, open("source/main_api.tl") as f3:
        schema = (f1.read() + f2.read() + f3.read()).splitlines()

    with open("template/type.txt") as f1, open("template/constructor.txt") as f2, open("template/function.txt") as f3:
        type_tmpl = f1.read()
        constructor_tmpl = f2.read()
        function_tmpl = f3.read()

    with open(NOTICE_PATH, encoding="utf-8") as f:
        notice = []

        for line in f.readlines():
            notice.append(f"#  {line}".strip())

        notice = "\n".join(notice)

    section = None
    layer = None
    namespaces = {"types": {}, "functions": {}}
    combinators = []
    types = {}
    functions = {}

    types_to_constructors = {}
    types_to_functions = {}
    constructors_to_functions = {}

    for line in schema:
        # Check for section changer lines
        section_match = SECTION_RE.match(line)
        if section_match:
            section = section_match.group(1)
            continue

        # Save the layer version
        layer_match = LAYER_RE.match(line)
        if layer_match:
            layer = layer_match.group(1)
            continue

        combinator_match = COMBINATOR_RE.match(line)
        if combinator_match:
            # noinspection PyShadowingBuiltins
            name, id, type = combinator_match.groups()
            namespace, _ = name.split(".") if "." in name else ("", name)

            # Pingu!
            has_flags = not not FLAGS_RE_3.findall(line)

            args = ARGS_RE.findall(line)

            # Rename to avoid collisions:
            if type == "Updates":
                type = "UpdatesT"

            # Fix arg name being "self" (reserved python keyword)
            for i, item in enumerate(args):
                if item[0] == "self":
                    args[i] = ("is_self", item[1])

            key = namespace or "_"

            if key not in namespaces[section]:
                namespaces[section][key] = []

            value = type if section == "types" else name

            if value not in namespaces[section][key]:
                namespaces[section][key].append(value)

            combinator = Combinator(
                section=section,
                name=name,
                id=f"0x{id}",
                has_flags=has_flags,
                args=args,
                type=type
            )

            combinators.append(combinator)

    for c in combinators:
        type = c.type

        if type.startswith("Vector"):
            type = type.split("<")[1][:-1]

        d = types_to_constructors if c.section == "types" else types_to_functions

        if type not in d:
            d[type] = []

        d[type].append(c.name)

    for k, v in types_to_constructors.items():
        for i in v:
            try:
                constructors_to_functions[i] = types_to_functions[k]
            except KeyError:
                pass

    for c in combinators:
        namespace, _ = c.name.split(".") if "." in c.name else ("", c.name)
        path = DESTINATION_PATH / c.section / namespace
        os.makedirs(path, exist_ok=True)

        init = path / "__init__.py"

        if not os.path.exists(init):
            with open(init, "w", encoding="utf-8") as f:
                f.write(notice + "\n\n")

        sorted_args = sort_args(c.args)

        arguments = (
            (", *, " if c.args else "") +
            (", ".join(
                [f"{i[0]}: {get_type_hint(i[1])}"
                 for i in sorted_args]
            ) if sorted_args else "")
        )

        fields = "\n        ".join(
            [f"self.{i[0]} = {i[0]}  # {i[1]}"
             for i in sorted_args]
        ) if sorted_args else "pass"

        write_types = read_types = "" if c.has_flags else "# No flags\n        "

        for arg_name, arg_type in c.args:
            flag = FLAGS_RE_2.findall(arg_type)

            if arg_name == "flags" and arg_type == "#":
                write_flags = []

                for i in c.args:
                    flag = FLAGS_RE.match(i[1])
                    if flag:
                        write_flags.append(f"flags |= (1 << {flag.group(1)}) if self.{i[0]} is not None else 0")

                write_flags = "\n        ".join([
                    "flags = 0",
                    "\n        ".join(write_flags),
                    "b.write(Int(flags))\n        "
                ])

                write_types += write_flags
                read_types += "flags = Int.read(b)\n        "

                continue

            if flag:
                index, flag_type = flag[0]

                if flag_type == "true":
                    read_types += "\n        "
                    read_types += f"{arg_name} = True if flags & (1 << {index}) else False"
                elif flag_type in CORE_TYPES:
                    write_types += "\n        "
                    write_types += f"if self.{arg_name} is not None:\n            "
                    write_types += f"b.write({flag_type.title()}(self.{arg_name}))\n        "

                    read_types += "\n        "
                    read_types += f"{arg_name} = {flag_type.title()}.read(b) if flags & (1 << {index}) else None"
                elif "vector" in flag_type.lower():
                    sub_type = arg_type.split("<")[1][:-1]

                    write_types += "\n        "
                    write_types += f"if self.{arg_name} is not None:\n            "
                    write_types += "b.write(Vector(self.{}{}))\n        ".format(
                        arg_name, f", {sub_type.title()}" if sub_type in CORE_TYPES else ""
                    )

                    read_types += "\n        "
                    read_types += "{} = TLObject.read(b{}) if flags & (1 << {}) else []\n        ".format(
                        arg_name, f", {sub_type.title()}" if sub_type in CORE_TYPES else "", index
                    )
                else:
                    write_types += "\n        "
                    write_types += f"if self.{arg_name} is not None:\n            "
                    write_types += f"b.write(self.{arg_name}.write())\n        "

                    read_types += "\n        "
                    read_types += f"{arg_name} = TLObject.read(b) if flags & (1 << {index}) else None\n        "
            else:
                if arg_type in CORE_TYPES:
                    write_types += "\n        "
                    write_types += f"b.write({arg_type.title()}(self.{arg_name}))\n        "

                    read_types += "\n        "
                    read_types += f"{arg_name} = {arg_type.title()}.read(b)\n        "
                elif "vector" in arg_type.lower():
                    sub_type = arg_type.split("<")[1][:-1]

                    write_types += "\n        "
                    write_types += "b.write(Vector(self.{}{}))\n        ".format(
                        arg_name, f", {sub_type.title()}" if sub_type in CORE_TYPES else ""
                    )

                    read_types += "\n        "
                    read_types += "{} = TLObject.read(b{})\n        ".format(
                        arg_name, f", {sub_type.title()}" if sub_type in CORE_TYPES else ""
                    )
                else:
                    write_types += "\n        "
                    write_types += f"b.write(self.{arg_name}.write())\n        "

                    read_types += "\n        "
                    read_types += f"{arg_name} = TLObject.read(b)\n        "

        combinator_name = camel(c.name.split(".")[-1])
        combinator_id = c.id
        slots = ", ".join([f'"{i[0]}"' for i in sorted_args])
        qualname = f"{c.section}.{namespace + ('.' if namespace else '')}{camel(c.name.split('.')[-1])}"
        return_arguments = ", ".join([f"{i[0]}={i[0]}" for i in sorted_args])

        if c.section == "types":
            type = c.type

            if type not in types:
                types[type] = []

            types[type].append((
                combinator_name,
                constructor_tmpl.format(
                    combinator_name=combinator_name,
                    type_name=f"T{camel(c.type.strip('.')[-1])}",
                    combinator_id=combinator_id,
                    arguments=arguments,
                    fields=fields,
                    read_types=read_types,
                    return_arguments=return_arguments,
                    write_types=write_types,
                    slots=slots,
                    qualname=qualname
                )
            ))
        else:
            functions[c.name] = function_tmpl.format(
                notice=notice,
                combinator_name=combinator_name,
                combinator_id=combinator_id,
                arguments=arguments,
                fields=fields,
                read_types=read_types,
                return_arguments=return_arguments,
                write_types=write_types,
                slots=slots,
                qualname=qualname
            )

    for type, constructors in types.items():
        type_namespace, type_name = type.split(".") if "." in type else ("", type)
        path = DESTINATION_PATH / "types" / type_namespace
        os.makedirs(path, exist_ok=True)

        with open(path / f"{snake(type_name)}.py", "w") as f:
            f.write(
                type_tmpl.format(
                    notice=notice,
                    type_name=f"T{camel(type_name)}",
                    constructors="\n\n\n".join([i[1] for i in constructors]),
                    union_types=", ".join([camel(i[0]) for i in constructors])
                )
            )

    for name, function in functions.items():
        namespace, name = name.split(".") if "." in name else ("", name)

        path = DESTINATION_PATH / "functions" / namespace
        os.makedirs(path, exist_ok=True)

        with open(path / f"{snake(name)}.py", "w") as f:
            f.write(function)

    with open(DESTINATION_PATH / "all.py", "w", encoding="utf-8") as f:
        f.write(notice + "\n\n")
        f.write(f"layer = {layer}\n\n")
        f.write("objects = {")

        for c in combinators:
            path = c.name.split(".")
            path[-1] = camel(path[-1])
            path = ".".join(path)

            f.write(f'\n    {c.id}: "pyrogram.api.{c.section}.{path}",')

        f.write('\n    0xbc799737: "pyrogram.api.core.BoolFalse",')
        f.write('\n    0x997275b5: "pyrogram.api.core.BoolTrue",')
        f.write('\n    0x1cb5c415: "pyrogram.api.core.Vector",')
        f.write('\n    0x73f1f8dc: "pyrogram.api.core.MsgContainer",')
        f.write('\n    0xae500895: "pyrogram.api.core.FutureSalts",')
        f.write('\n    0x0949d9dc: "pyrogram.api.core.FutureSalt",')
        f.write('\n    0x3072cfa1: "pyrogram.api.core.GzipPacked",')
        f.write('\n    0x5bb8e511: "pyrogram.api.core.Message",')

        f.write("\n}\n")

    for section, namespaces in namespaces.items():
        for name, types in namespaces.items():
            if name == "_":
                path = DESTINATION_PATH / section / "__init__.py"
                with open(path, "a", encoding="utf-8") as f:
                    f.write(f"from . import {', '.join([i for i in namespaces if i != '_'])}\n")
            else:
                path = DESTINATION_PATH / section / name / "__init__.py"

            with open(path, "a", encoding="utf-8") as f:
                for type in types:
                    namespace, name = type.split(".") if "." in type else ("", type)

                    if section == "types":
                        constructors_imports = []
                        for i in types_to_constructors[type]:
                            a, b = i.split(".") if "." in i else ("", i)
                            constructors_imports.append(camel(b))

                        imports = f"T{camel(name)}, {', '.join(constructors_imports)}"
                        f.write(f"from .{snake(name)} import {imports}\n")
                    else:
                        f.write(f"from .{snake(name)} import {camel(name)}\n")


if "__main__" == __name__:
    HOME_PATH = Path(".")
    DESTINATION_PATH = Path("../../pyrogram/api")
    NOTICE_PATH = Path("../../NOTICE")

    start()
