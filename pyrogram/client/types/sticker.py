class Sticker:
    def __init__(self,
                 file_id: str,
                 width: int,
                 height: int,
                 thumb: "PhotoSize" = None,
                 emoji: str = None,
                 set_name: str = None,
                 mask_position: "MaskPosition" = None,
                 file_size: int = None):
        self.file_id = file_id
        self.width = width
        self.height = height
        self.thumb = thumb
        self.emoji = emoji
        self.set_name = set_name
        self.mask_position = mask_position
        self.file_size = file_size
