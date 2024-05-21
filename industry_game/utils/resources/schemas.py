from pydantic import BaseModel, ConfigDict, PositiveInt

from industry_game.utils.resources.models import ResourceType


class ResourceModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    resource: ResourceType
    amount: PositiveInt
