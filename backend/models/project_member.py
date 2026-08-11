from typing import Optional
from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.models.base import BaseModel

class ProjectMember(BaseModel):
    __tablename__ = "project_members"
    __table_args__ = (
        UniqueConstraint("project_id", "user_id", name="unique_project_user_member"),
    )

    project_id: Mapped[str] = mapped_column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    project_role: Mapped[str] = mapped_column(String(50), default="PROJECT_MANAGER", nullable=False)

    # Relationships
    project: Mapped["Project"] = relationship("Project", backref="members")
    user: Mapped["User"] = relationship("User", backref="memberships")
