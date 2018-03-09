class Voice:
    def __init__(self,
                 file_id: str,
                 duration: int,
                 mime_type: str = None,
                 file_size: int = None):
        self.file_id = file_id
        self.duration = duration
        self.mime_type = mime_type
        self.file_size = file_size
