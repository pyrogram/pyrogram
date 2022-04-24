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

import pyrogram
from pyrogram import raw
from pyrogram import types
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

        audio (:obj:`~pyrogram.types.Audio`, *optional*):
            Webpage preview is an audio file, information about the file.

        document (:obj:`~pyrogram.types.Document`, *optional*):
            Webpage preview is a general file, information about the file.

        photo (:obj:`~pyrogram.types.Photo`, *optional*):
            Webpage preview is a photo, information about the photo.

        animation (:obj:`~pyrogram.types.Animation`, *optional*):
            Webpage preview is an animation, information about the animation.

        video (:obj:`~pyrogram.types.Video`, *optional*):
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
        client: "pyrogram.Client" = None,
        id: str,
        url: str,
        display_url: str,
        type: str = None,
        site_name: str = None,
        title: str = None,
        description: str = None,
        audio: "types.Audio" = None,
        document: "types.Document" = None,
        photo: "types.Photo" = None,
        animation: "types.Animation" = None,
        video: "types.Video" = None,
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
    def _parse(client, webpage: "raw.types.WebPage") -> "WebPage":
        audio = None
        document = None
        photo = None
        animation = None
        video = None

        if isinstance(webpage.photo, raw.types.Photo):
            photo = types.Photo._parse(client, webpage.photo)

        doc = webpage.document

        if isinstance(doc, raw.types.Document):
            attributes = {type(i): i for i in doc.attributes}

            file_name = getattr(
                attributes.get(
                    raw.types.DocumentAttributeFilename, None
                ), "file_name", None
            )

            if raw.types.DocumentAttributeAudio in attributes:
                audio_attributes = attributes[raw.types.DocumentAttributeAudio]
                audio = types.Audio._parse(client, doc, audio_attributes, file_name)

            elif raw.types.DocumentAttributeAnimated in attributes:
                video_attributes = attributes.get(raw.types.DocumentAttributeVideo, None)
                animation = types.Animation._parse(client, doc, video_attributes, file_name)

            elif raw.types.DocumentAttributeVideo in attributes:
                video_attributes = attributes[raw.types.DocumentAttributeVideo]
                video = types.Video._parse(client, doc, video_attributes, file_name)

            else:
                document = types.Document._parse(client, doc, file_name)

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
