from . import Animation


class Game:
    def __init__(self,
                 title: str,
                 description: str,
                 photo: list,
                 text: str = None,
                 text_entities: list = None,
                 animation: Animation = None):
        self.title = title
        self.description = description
        self.photo = photo
        self.text = text
        self.text_entities = text_entities
        self.animation = animation
