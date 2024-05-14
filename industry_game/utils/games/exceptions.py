from industry_game.utils.exceptions import IndustryGameException


class GameNotFoundException(IndustryGameException):
    def __init__(self, game_id: int) -> None:
        super().__init__(f"Game with id {game_id} not found")
