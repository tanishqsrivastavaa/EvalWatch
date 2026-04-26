from sqlmodel import SQLModel
from datetime import datetime


class input_lmm_traces(SQLModel):
    prompt: str
    response : str
    latency: int
    model_name : str
    token_usage: int
  