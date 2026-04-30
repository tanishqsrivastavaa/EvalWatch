from typing import  Optional
from fastapi import Depends, APIRouter
from sqlmodel import Session, select
from app.db.session import get_session
from app.models.observe import llm_traces
from app.schemas.observe import input_lmm_traces
from app.crud.user import get_user_by_email #did not add user auth to protect the endpoints.


MAX_LIMIT = 10
OFFSET = 0

router = APIRouter()

@router.post("/trace_llm")
def insert_llm_trace(
    llm_object : input_lmm_traces,
    session : Session = Depends(get_session)
    #current_user = Depends(get_user_by_email),
):
    
    new_llm_object = llm_traces(
        prompt = llm_object.prompt,
        response = llm_object.response,
        latency_ms = llm_object.latency,
        model_name=llm_object.model_name,
        token_usage = llm_object.token_usage,
    )

    session.add(new_llm_object)
    session.commit()
    session.refresh(new_llm_object)

    return {"final_message" : "LLM data inserted successfully!!!"}
    


@router.get("/all_logs")
def get_all_llm_trace(
    model_name: Optional[str] = None,
    min_latency : Optional[int] = None,
    limit : Optional[int] = 10,
    offset: Optional[int] = 0,
    session : Session = Depends(get_session)
):
    statement = select(llm_traces)

    #FILTERS
    if model_name:
        statement = statement.where(llm_traces.model_name == model_name)

    if min_latency:
        statement  = statement.where(llm_traces.latency_ms >= min_latency) 

    #PAGINATION
    limit = min(limit,MAX_LIMIT)
    statement = statement.offset(offset)
    statement = statement.limit(limit)

    result = session.exec(statement)
    data = result.all()
    return data