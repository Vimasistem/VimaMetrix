from sqlalchemy.event import listens_for

from .base import Column, db


class TimestampMixin:
    updated_at = Column(db.DateTime(True), default=db.func.now(), nullable=False)
    created_at = Column(db.DateTime(True), default=db.func.now(), nullable=False)


@listens_for(TimestampMixin, "before_update", propagate=True)
def timestamp_before_update(mapper, connection, target):
    # Check if we really want to update the updated_at value
    if hasattr(target, "skip_updated_at"):
        return

    target.updated_at = db.func.now()


class BelongsToOrgMixin:
    @classmethod
    def get_by_id_and_org(cls, object_id, org, org_cls=None):
        query = cls.query.filter(cls.id == object_id)
        if org_cls is None:
            query = query.filter(cls.org == org)
        else:
            query = query.join(org_cls).filter(org_cls.org == org)
        return query.one()
    
    @classmethod
    def get_by_id_when_no_latest(cls, query):
        query_runner = query.data_source.query_runner

        data = query_runner.run_query(query.query_text, None)
        return data
