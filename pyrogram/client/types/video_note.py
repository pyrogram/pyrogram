from . import PhotoSize


class VideoNote:
    def __init__(self,
                 file_id: str,
                 length: int,
                 duration: int,
                 thumb: PhotoSize = None,
                 file_size: int = None):
        self.file_id = file_id
        self.length = length
        self.duration = duration
        self.thumb = thumb
        self.file_size = file_size
