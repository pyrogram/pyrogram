class Venue:
    def __init__(self,
                 location: "Location",
                 title: str,
                 address: str,
                 foursquare_id: str = None):
        self.location = location
        self.title = title
        self.address = address
        self.foursquare_id = foursquare_id
