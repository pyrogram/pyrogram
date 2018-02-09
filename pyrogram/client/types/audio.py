class Audio:
    def __init__(self,
                 file_id: str,
                 duration: int = None,
                 performer: str = None,
                 title: str = None,
                 mime_type: str = None,
                 file_size: str = None):
        self.file_id = file_id
        self.duration = duration
        self.performer = performer
        self.title = title
        self.mime_type = mime_type
        self.file_size = file_size
