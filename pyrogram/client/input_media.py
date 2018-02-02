class InputMedia:
    class Photo:
        def __init__(self,
                     media: str,
                     caption: str = "",
                     parse_mode: str = ""):
            self.media = media
            self.caption = caption
            self.parse_mode = parse_mode

    class Video:
        def __init__(self,
                     media: str,
                     caption: str = "",
                     parse_mode: str = "",
                     width: int = 0,
                     height: int = 0,
                     duration: int = 0):
            self.media = media
            self.caption = caption
            self.parse_mode = parse_mode
            self.width = width
            self.height = height
            self.duration = duration
