from collections import deque
from datetime import UTC, datetime

from industry_game.db.models import GameStatus
from industry_game.utils.districts.models import District
from industry_game.utils.games.models import Game, ProcessGame
from industry_game.utils.games.session import SESSIONS, SessionController
from industry_game.utils.maps.models import Map
from industry_game.utils.notifications.models import Notification
from industry_game.utils.players.models import Player, PlayerRoles


def create_game() -> ProcessGame:
    user_ids = [
        [2, PlayerRoles.DIRECTOR],
        [3, PlayerRoles.FINANCIER],
        [4, PlayerRoles.HR_MANAGER],
        [5, PlayerRoles.TERRITORY_MANAGER],
        [6, PlayerRoles.DEVELOPER],
    ]

    game_id = 1
    game = ProcessGame(
        game=Game(
            id=game_id,
            name="Тестовая игра",
            description="Это игра происходящая на Марсе",
            created_by_id=0,
            status=GameStatus.STARTED,
            started_at=datetime.now(tz=UTC),
            finished_at=None,
            created_at=datetime.now(tz=UTC),
            updated_at=datetime.now(tz=UTC),
        ),
        event_queue=deque(),
        districts={
            1: District(
                game_district_id=1,
                name="Аргон",
                players=[
                    Player(user_id=user_id, role=role)
                    for user_id, role in user_ids
                ],
            ),
            2: District(
                game_district_id=8,
                name="Дагон",
                players=[
                    Player(user_id=7, role=PlayerRoles.HR_MANAGER),
                ],
            ),
        },
        map=Map(),
        session_controller=SessionController(sessions=SESSIONS),
    )
    for district in game.districts.values():
        district.balance.init()
        district.people.init()
    game.districts[1].players[PlayerRoles.FINANCIER].add_notification(
        Notification(title="Hello worls", message="Hello world")
    )

    for x, y in ((0, 0), (0, 1), (1, 1), (1, 2), (1, 3)):
        game.map.capture_hexagon(x, y, game.districts[1])

    return game
