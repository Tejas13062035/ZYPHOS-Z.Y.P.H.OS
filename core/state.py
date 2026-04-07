from pydantic import BaseModel
from typing import List, Optional

class ZypState(BaseModel):
    goal: str
    current_step: Optional[str] = None
    completed_steps: List[str] = []
    blocked: bool = False
