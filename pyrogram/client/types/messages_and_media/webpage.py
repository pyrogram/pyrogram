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

import pyrogram
from pyrogram.api import types
from ..object import Object


class WebPage(Object):
    # TODO: hash, cached_page
    """A webpage preview

    Parameters:
        id (``str``):
            Unique identifier for this webpage.

        url (``str``):
            Full URL for this webpage.

        display_url (``str``):
            Display URL for this webpage.

        type (``str``, *optional*):
            Type of webpage preview, known types (at the time of writing) are:
            *"article"*, *"photo"*, *"gif"*, *"video"* and *"document"*,
            *"telegram_user"*, *"telegram_bot"*, *"telegram_channel"*, *"telegram_megagroup"*.

        site_name (``str``, *optional*):
            Webpage site name.

        title (``str``, *optional*):
            Title of this webpage.

        description (``str``, *optional*):
            Description of this webpage.

        audio (:obj:`Audio`, *optional*):
            Webpage preview is an audio file, information about the file.

        document (:obj:`Document`, *optional*):
            Webpage preview is a general file, information about the file.

        photo (:obj:`Photo`, *optional*):
            Webpage preview is a photo, information about the photo.

        animation (:obj:`Animation`, *optional*):
            Webpage preview is an animation, information about the animation.

        video (:obj:`Video`, *optional*):
            Webpage preview is a video, information about the video.

        embed_url (``str``, *optional*):
            Embedded content URL.

        embed_type (``str``, *optional*):
            Embedded content type, like `iframe`

        embed_width (``int``, *optional*):
            Embedded content width.

        embed_height (``int``, *optional*):
            Embedded content height.

        duration (``int``, *optional*):
            Unknown at the time of writing.

        author (``str``, *optional*):
            Author of the webpage, eg the Twitter user for a tweet, or the author in an article.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.BaseClient" = None,
        id: str,
        url: str,
        display_url: str,
        type: str = None,
        site_name: str = None,
        title: str = None,
        description: str = None,
        audio: "pyrogram.Audio" = None,
        document: "pyrogram.Document" = None,
        photo: "pyrogram.Photo" = None,
        animation: "pyrogram.Animation" = None,
        video: "pyrogram.Video" = None,
        embed_url: str = None,
        embed_type: str = None,
        embed_width: int = None,
        embed_height: int = None,
        duration: int = None,
        author: str = None
    ):
        super().__init__(client)

        self.id = id
        self.url = url
        self.display_url = display_url
        self.type = type
        self.site_name = site_name
        self.title = title
        self.description = description
        self.audio = audio
        self.document = document
        self.photo = photo
        self.animation = animation
        self.video = video
        self.embed_url = embed_url
        self.embed_type = embed_type
        self.embed_width = embed_width
        self.embed_height = embed_height
        self.duration = duration
        self.author = author

    @staticmethod
    def _parse(client, webpage: types.WebPage) -> "WebPage":
        audio = None
        document = None
        photo = None
        animation = None
        video = None

        if isinstance(webpage.photo, types.Photo):
            photo = pyrogram.Photo._parse(client, webpage.photo)

        doc = webpage.document

        if isinstance(doc, types.Document):
            attributes = {type(i): i for i in doc.attributes}

            file_name = getattr(
                attributes.get(
                    types.DocumentAttributeFilename, None
                ), "file_name", None
            )

            if types.DocumentAttributeAudio in attributes:
                audio_attributes = attributes[types.DocumentAttributeAudio]
                audio = pyrogram.Audio._parse(client, doc, audio_attributes, file_name)

            elif types.DocumentAttributeAnimated in attributes:
                video_attributes = attributes.get(types.DocumentAttributeVideo, None)
                animation = pyrogram.Animation._parse(client, doc, video_attributes, file_name)

            elif types.DocumentAttributeVideo in attributes:
                video_attributes = attributes[types.DocumentAttributeVideo]
                video = pyrogram.Video._parse(client, doc, video_attributes, file_name)

            else:
                document = pyrogram.Document._parse(client, doc, file_name)

        return WebPage(
            id=str(webpage.id),
            url=webpage.url,
            display_url=webpage.display_url,
            type=webpage.type,
            site_name=webpage.site_name,
            title=webpage.title,
            description=webpage.description,
            audio=audio,
            document=document,
            photo=photo,
            animation=animation,
            video=video,
            embed_url=webpage.embed_url,
            embed_type=webpage.embed_type,
            embed_width=webpage.embed_width,
            embed_height=webpage.embed_height,
            duration=webpage.duration,
            author=webpage.author
        )
