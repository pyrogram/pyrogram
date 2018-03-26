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
        all_members_are_administrators=chat.admins_enabled
    )


def parse_channel_chat(channel: types.Channel):
    return pyrogram.Chat(
        id=int("-100" + str(channel.id)),
        type="supergroup" if channel.megagroup else "channel",
        title=channel.title,
        username=channel.username
    )


def parse_message(message: types.Message, users: dict, chats: dict):
    from_user = users.get(message.from_id, None)  # type: types.User

    if isinstance(message.to_id, types.PeerUser):
        chat = parse_user_chat(users[message.to_id.user_id])
    elif isinstance(message.to_id, types.PeerChat):
        chat = parse_chat_chat(chats[message.to_id.chat_id])
    else:
        chat = parse_channel_chat(chats[message.to_id.channel_id])

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

    return pyrogram.Message(
        message_id=message.id,
        date=message.date,
        chat=chat,
        from_user=parse_user(from_user),
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
        edit_date=message.edit_date
    )
