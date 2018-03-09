class MaskPosition:
    def __init__(self,
                 point: str,
                 x_shift: float,
                 y_shift: float,
                 scale: float):
        self.point = point
        self.x_shift = x_shift
        self.y_shift = y_shift
        self.scale = scale
