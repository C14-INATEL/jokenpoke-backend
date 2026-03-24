class Pokemon:
    def __init__(
        self,
        id: int,
        original_name: str,
        name: str,
        move: str,
        description: str,
    ):
        self.id = id
        self.original_name = original_name
        self.name = name
        self.move = move
        self.description = description