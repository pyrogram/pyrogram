class Video:
    def __init__(self,
                 file_id: str,
                 width: int,
                 height: int,
                 duration: int,
                 thumb: "PhotoSize" = None,
                 mime_type: str = None,
                 file_size: int = None):
        self.file_id = file_id
        self.width = width
        self.height = height
        self.duration = duration
        self.thumb = thumb
        self.mime_type = mime_type
        self.file_size = file_size
