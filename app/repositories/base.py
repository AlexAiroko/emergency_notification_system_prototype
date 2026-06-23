from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session


class BaseRepository:
    model = None
    
    def __init__(self, session: Session) -> None:
        self.session = session

    def flush(self) -> None:
        self.session.flush()
    
    def create(self, **kwargs):
        obj = self.model(**kwargs)
        self.session.add(obj)
        self.flush()
        return obj
    
    def get(self, obj_id: int):
        stmt = (
            select(self.model)
            .where(self.model.id == obj_id)
        )
        res = self.session.execute(stmt)
        obj = res.scalar_one_or_none()
        return obj
    
    def get_many(self, limit: int = 20, offset: int = 0):
        stmt = (
            select(self.model)
            .order_by(self.model.id)
            .limit(limit)
            .offset(offset)
        )
        res = self.session.execute(stmt)
        objs = list(res.scalars().all())
        return objs
    
    def update(
        self,
        obj_id: int,
        **kwargs,
    ):
        stmt = (
            update(self.model)
            .where(self.model.id == obj_id)
            .values(**kwargs)
        )
        self.session.execute(stmt)

    def delete(self, obj_id: int) -> None:
        stmt = (
            delete(self.model)
            .where(self.model.id == obj_id)
        )
        self.session.execute(stmt)
