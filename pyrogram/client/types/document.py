from . import PhotoSize


class Document:
    def __init__(self,
                 file_id: str,
                 thumb: PhotoSize = None,
                 file_name: str = None,
                 mime_type: str = None,
                 file_size: int = None):
        self.file_id = file_id
        self.thumb = thumb
        self.file_name = file_name
        self.mime_type = mime_type
        self.file_size = file_size
