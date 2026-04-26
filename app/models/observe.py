from sqlmodel import SQLModel, Field
from uuid import UUID,uuid4
from datetime import datetime, timezone

class llm_traces(SQLModel,table = True):
    id : int | None = Field(default = None, primary_key=True) #generating in backend
    prompt: str 
    response: str
    latency_ms: int
    model_name : str
    token_usage: int
    trace_id: UUID = Field(default_factory=uuid4) #generating in backend
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False) #generating in backend
