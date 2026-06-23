from sqlalchemy import select

from app.repositories.base import BaseRepository


class ActiveRepository(BaseRepository):
    """
    Repository for models with is_active field
    """
    
    def get_active(
        self,
        limit: int = 20,
        offset: int = 0,
    ):
        stmt = (
            select(self.model)
            .where(self.model.is_active)
            .order_by(self.model.id)
            .limit(limit)
            .offset(offset)
        )
        res = self.session.execute(stmt)
        objs = list(res.scalars().all())
        return objs
    
    def activate(self, obj_id: int) -> None:
        self.update(obj_id, is_active=True)
    
    def deactivate(self, obj_id: int) -> None:
        self.update(obj_id, is_active=False)
