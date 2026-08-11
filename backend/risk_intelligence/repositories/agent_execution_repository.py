from typing import List
from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from backend.repositories.base_repository import BaseRepository
from backend.risk_intelligence.models.agent_execution import AgentExecution

class AgentExecutionRepository(BaseRepository[AgentExecution]):
    def __init__(self, session: Session):
        super().__init__(AgentExecution, session)

    def get_by_assessment(self, assessment_id: str) -> List[AgentExecution]:
        stmt = (
            select(AgentExecution)
            .where(AgentExecution.assessment_id == assessment_id)
            .where(AgentExecution.is_deleted == False)
            .order_by(desc(AgentExecution.executed_at))
        )
        return list(self.session.execute(stmt).scalars().all())
