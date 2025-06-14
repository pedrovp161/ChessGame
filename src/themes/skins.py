class Skins:
    def __init__(self):
        self.dict_def_of_skins = {
            "default": {
                "name": "Default",
                "description": "The default skin.",
                "author": "Pedro Videira Pinho",
                "version": "1.0",
                "path": "/path/to/default/skin"
            },
            "dark_mode": {
                "name": "Dark Mode",
                "description": "A dark-themed skin.",
                "author": "Pedro Videira Pinho",
                "version": "1.0",
                "path": "/path/to/dark_mode/skin"
            }
        }
        
    def default_skin(self):
        # Colors
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        LIGHT_SQUARE = (240, 217, 181)
        DARK_SQUARE = (181, 136, 99)
        return WHITE, BLACK, LIGHT_SQUARE, DARK_SQUARE