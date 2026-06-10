"""
CRUD operations for the poll index table.

NO COMMITS IN CRUD
"""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from core.enums import PollType
from models.polls import Polls


class PollRepository:
    @staticmethod
    def get_poll_entry(
        session: Session,
        poll_from: UUID,
        poll_to: UUID,
        poll_type: PollType,
    ) -> Polls | None:
        stmt = select(Polls).where(
            Polls.poll_from == poll_from,
            Polls.poll_to == poll_to,
            Polls.poll_type == poll_type,
        )
        return session.scalar(stmt)

    @staticmethod
    def list_pending_for_user(
        session: Session,
        user_id: UUID,
        poll_type: PollType | None = None,
    ) -> list[Polls]:
        stmt = select(Polls).where(Polls.poll_to == user_id)
        if poll_type is not None:
            stmt = stmt.where(Polls.poll_type == poll_type)

        return list(session.scalars(stmt).all())

    @staticmethod
    def append_record(
        session: Session,
        poll_from: UUID,
        poll_to: UUID,
        poll_type: PollType,
        record_id: int,
    ) -> Polls:
        poll = PollRepository.get_poll_entry(session, poll_from, poll_to, poll_type)

        if poll is None:
            poll = Polls(
                poll_from=poll_from,
                poll_to=poll_to,
                poll_type=poll_type,
                poll_count=1,
                poll_id=[record_id],
            )
            session.add(poll)
        else:
            current_ids = list(poll.poll_id or [])
            if record_id not in current_ids:
                current_ids.append(record_id)
                poll.poll_id = current_ids
                poll.poll_count = len(current_ids)

        session.flush()
        session.refresh(poll)
        return poll

    @staticmethod
    def remove_record(
        session: Session,
        poll_from: UUID,
        poll_to: UUID,
        poll_type: PollType,
        record_id: int,
    ) -> None:
        poll = PollRepository.get_poll_entry(session, poll_from, poll_to, poll_type)
        if not poll:
            return

        current_ids = list(poll.poll_id or [])
        if record_id not in current_ids:
            return

        current_ids.remove(record_id)
        poll.poll_count = len(current_ids)
        poll.poll_id = current_ids

        if poll.poll_count == 0:
            session.delete(poll)
        else:
            session.flush()
            session.refresh(poll)


__all__ = ["PollRepository"]
