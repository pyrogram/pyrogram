from . import Message


class Update:
    """This object represents an incoming update.
    At most one of the optional parameters can be present in any given update.


    Args:
        message (:obj:`Message <pyrogram.Message>`):

        edited_message ():

        channel_post ():

        edited_channel_post ():

    """

    def __init__(self,
                 message: Message = None,
                 edited_message: Message = None,
                 channel_post: Message = None,
                 edited_channel_post: Message = None):
        self.message = message
        self.edited_message = edited_message
        self.channel_post = channel_post
        self.edited_channel_post = edited_channel_post
