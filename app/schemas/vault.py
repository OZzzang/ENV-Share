from typing import Annotated
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field

class VaultCreate(BaseModel):
    name: Annotated[str, Field(max_length=64, min_length=1, pattern=r"^[a-z0-9_/-]+$")]

class VaultOut(BaseModel):
    id: UUID
    name: str
    created_at: datetime
