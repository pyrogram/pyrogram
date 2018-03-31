from base64 import b64encode, b64decode
from struct import pack

import pyrogram
from pyrogram.api import types

ENTITIES = {
    types.MessageEntityMention.ID: "mention",
    types.MessageEntityHashtag.ID: "hashtag",
    types.MessageEntityBotCommand.ID: "bot_command",
    types.MessageEntityUrl.ID: "url",
    types.MessageEntityEmail.ID: "email",
    types.MessageEntityBold.ID: "bold",
    types.MessageEntityItalic.ID: "italic",
    types.MessageEntityCode.ID: "code",
    types.MessageEntityPre.ID: "pre",
    types.MessageEntityTextUrl.ID: "text_link",
}


def parse_entities(entities: list):
    output_entities = []

    for entity in entities:
        entity_type = ENTITIES.get(entity.ID, None)

        if entity_type:
            output_entities.append(pyrogram.MessageEntity(
                type=entity_type,
                offset=entity.offset,
                length=entity.length,
                url=getattr(entity, "url", None)
            ))

    return output_entities


def parse_user(user: types.User):
    return pyrogram.User(
        id=user.id,
        is_bot=user.bot,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        language_code=user.lang_code
    ) if user else None


def parse_chat(message: types.Message, users: dict, chats: dict):
    if isinstance(message.to_id, types.PeerUser):
        return parse_user_chat(users[message.from_id])
    elif isinstance(message.to_id, types.PeerChat):
        return parse_chat_chat(chats[message.to_id.chat_id])
    else:
        return parse_channel_chat(chats[message.to_id.channel_id])


def parse_user_chat(user: types.User):
    return pyrogram.Chat(
        id=user.id,
        type="private",
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    )


def parse_chat_chat(chat: types.Chat):
    return pyrogram.Chat(
        id=-chat.id,
        type="group",
        title=chat.title,
        all_members_are_administrators=not chat.admins_enabled
    )


def parse_channel_chat(channel: types.Channel):
    return pyrogram.Chat(
        id=int("-100" + str(channel.id)),
        type="supergroup" if channel.megagroup else "channel",
        title=channel.title,
        username=channel.username
    )


def parse_message(message: types.Message, users: dict, chats: dict):
    entities = parse_entities(message.entities)

    forward_from = None
    forward_from_chat = None
    forward_from_message_id = None
    forward_signature = None
    forward_date = None

    forward_header = message.fwd_from  # type: types.MessageFwdHeader

    if forward_header:
        forward_date = forward_header.date

        if forward_header.from_id:
            forward_from = parse_user(users[forward_header.from_id])
        else:
            forward_from_chat = parse_channel_chat(chats[forward_header.channel_id])
            forward_from_message_id = forward_header.channel_post
            forward_signature = forward_header.post_author

    photo = None

    media = message.media

    if media:
        if isinstance(media, types.MessageMediaPhoto):
            photo = media.photo

            if isinstance(photo, types.Photo):
                sizes = photo.sizes
                photo_sizes = []

                for size in sizes:
                    if isinstance(size, (types.PhotoSize, types.PhotoCachedSize)):
                        location = size.location

                        if isinstance(location, types.FileLocation):
                            photo_size = pyrogram.PhotoSize(
                                file_id=encode(
                                    pack(
                                        "<iiqqqqi",
                                        2,
                                        location.dc_id,
                                        photo.id,
                                        photo.access_hash,
                                        location.volume_id,
                                        location.secret,
                                        location.local_id
                                    )
                                ),
                                width=size.w,
                                height=size.h,
                                file_size=size.size
                            )

                            photo_sizes.append(photo_size)

                photo = photo_sizes

    return pyrogram.Message(
        message_id=message.id,
        date=message.date,
        chat=parse_chat(message, users, chats),
        from_user=parse_user(users.get(message.from_id, None)),
        text=message.message or None if message.media is None else None,
        caption=message.message or None if message.media is not None else None,
        entities=entities or None if message.media is None else None,
        caption_entities=entities or None if message.media is not None else None,
        author_signature=message.post_author,
        forward_from=forward_from,
        forward_from_chat=forward_from_chat,
        forward_from_message_id=forward_from_message_id,
        forward_signature=forward_signature,
        forward_date=forward_date,
        edit_date=message.edit_date,
        photo=photo
    )


def parse_message_service(message: types.MessageService, users: dict, chats: dict):
    action = message.action

    new_chat_members = None
    left_chat_member = None
    new_chat_title = None
    delete_chat_photo = None
    migrate_to_chat_id = None
    migrate_from_chat_id = None
    group_chat_created = None

    if isinstance(action, types.MessageActionChatAddUser):
        new_chat_members = [parse_user(users[i]) for i in action.users]
    elif isinstance(action, types.MessageActionChatJoinedByLink):
        new_chat_members = [parse_user(users[action.inviter_id])]
    elif isinstance(action, types.MessageActionChatDeleteUser):
        left_chat_member = parse_user(users[action.user_id])
    elif isinstance(action, types.MessageActionChatEditTitle):
        new_chat_title = action.title
    elif isinstance(action, types.MessageActionChatDeletePhoto):
        delete_chat_photo = True
    elif isinstance(action, types.MessageActionChatMigrateTo):
        migrate_to_chat_id = action.channel_id
    elif isinstance(action, types.MessageActionChannelMigrateFrom):
        migrate_from_chat_id = action.chat_id
    elif isinstance(action, types.MessageActionChatCreate):
        group_chat_created = True
    else:
        return None

    return pyrogram.Message(
        message_id=message.id,
        date=message.date,
        chat=parse_chat(message.to_id, users, chats),
        from_user=parse_user(users.get(message.from_id, None)),
        new_chat_members=new_chat_members,
        left_chat_member=left_chat_member,
        new_chat_title=new_chat_title,
        delete_chat_photo=delete_chat_photo,
        migrate_to_chat_id=migrate_to_chat_id,
        migrate_from_chat_id=migrate_from_chat_id,
        group_chat_created=group_chat_created
    )


def decode(s):
    s = b64decode(s + "=" * (-len(s) % 4), "-_")
    r = b""

    assert s[-1] == 2

    i = 0
    while i < len(s) - 1:
        if s[i] != 0:
            r += bytes([s[i]])
        else:
            r += b"\x00" * s[i + 1]
            i += 1

        i += 1

    return r


def encode(s):
    r = b""
    n = 0

    for i in s + bytes([2]):
        if i == 0:
            n += 1
        else:
            if n:
                r += b"\x00" + bytes([n])
                n = 0

            r += bytes([i])

    return b64encode(r, b"-_").decode().rstrip("=")
