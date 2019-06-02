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

import datetime
import os

canonical = "https://docs.pyrogram.org/"

dirs = {
    ".": ("weekly", 1.0),
    "intro": ("weekly", 0.9),
    "start": ("weekly", 0.9),
    "api": ("weekly", 0.8),
    "topics": ("weekly", 0.8),
    "telegram": ("weekly", 0.6)
}


def now():
    return datetime.datetime.today().strftime("%Y-%m-%d")


with open("sitemap.xml", "w") as f:
    f.write('<?xml version="1.0" encoding="utf-8"?>\n')
    f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')

    urls = []


    def search(path):
        try:
            for j in os.listdir(path):
                search("{}/{}".format(path, j))
        except NotADirectoryError:
            if not path.endswith(".rst"):
                return

            path = path.split("/")[1:]

            if path[0].endswith(".rst"):
                folder = "."
            else:
                folder = path[0]

            path = "{}{}".format(canonical, "/".join(path))[:-len(".rst")]

            if path.endswith("index"):
                path = path[:-len("index")]

            urls.append((path, now(), *dirs[folder]))


    search("source")

    urls.sort(key=lambda x: x[3], reverse=True)

    for i in urls:
        f.write("    <url>\n")
        f.write("        <loc>{}</loc>\n".format(i[0]))
        f.write("        <lastmod>{}</lastmod>\n".format(i[1]))
        f.write("        <changefreq>{}</changefreq>\n".format(i[2]))
        f.write("        <priority>{}</priority>\n".format(i[3]))
        f.write("    </url>\n\n")

    f.write("</urlset>")
