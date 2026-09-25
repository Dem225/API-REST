from pydantic import BaseModel, Field


class CreateTaskValide(BaseModel):

    title: str = Field()

    description: str = Field()

    priority: str = Field()

    completed: bool = Field(
        default=False
    )
