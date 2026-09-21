from pydantic import BaseModel, Field


class CreateTask(BaseModel):

    title: str = Field()

    description: str = Field()

    priority: str = Field()

    completed: bool = Field(
        default=False
    )

    userId: int = Field()