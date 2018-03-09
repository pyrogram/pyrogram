class StickerSet:
    def __init__(self,
                 name: str,
                 title: str,
                 contain_masks: bool,
                 stickers: list):
        self.name = name
        self.title = title
        self.contain_masks = contain_masks
        self.stickers = stickers
