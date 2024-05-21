from pydantic import BaseModel, PositiveInt

from industry_game.utils.people.models import HumanType


class HumanModel(BaseModel):
    type: HumanType
    amount: PositiveInt
