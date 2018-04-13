from pyrogram.api import types


def get_peer_id(input_peer) -> int:
    return (
        input_peer.user_id if isinstance(input_peer, types.InputPeerUser)
        else -input_peer.chat_id if isinstance(input_peer, types.InputPeerChat)
        else int("-100" + str(input_peer.channel_id))
    )


def get_input_peer(peer_id: int, access_hash: int = 0):
    return (
        types.InputPeerUser(peer_id, access_hash) if peer_id > 0
        else types.InputPeerChannel(int(str(peer_id).lstrip("-100")), access_hash) if str(peer_id).startswith("-100")
        else types.InputPeerChat(-peer_id)
    )
