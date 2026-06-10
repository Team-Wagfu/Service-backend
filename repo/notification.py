"""
CRUD operations for notification records.

NO COMMITS IN CRUD
"""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.polls import PollNotification
from schemas.notifications import SendNotification


class NotificationRepository:
    @staticmethod
    def create_notification(
        session: Session,
        sender_id: UUID,
        payload: SendNotification,
    ) -> PollNotification:
        notification = PollNotification(
            poll_from=sender_id,
            poll_to=payload.recipient_id,
            content=payload.content,
            priority=payload.priority,
        )

        session.add(notification)
        session.flush()
        session.refresh(notification)

        return notification

    @staticmethod
    def get_by_id(
        session: Session, notification_id: int
    ) -> PollNotification | None:
        stmt = select(PollNotification).where(PollNotification.id == notification_id)
        return session.scalar(stmt)

    @staticmethod
    def list_for_recipient(
        session: Session,
        recipient_id: UUID,
        unread_only: bool = False,
    ) -> list[PollNotification]:
        stmt = select(PollNotification).where(PollNotification.poll_to == recipient_id)
        if unread_only:
            stmt = stmt.where(PollNotification.read.is_(False))

        return list(session.scalars(stmt).all())

    @staticmethod
    def mark_read(session: Session, notification: PollNotification) -> PollNotification:
        notification.read = True
        session.flush()
        session.refresh(notification)
        return notification

    @staticmethod
    def delete_notification(
        session: Session, notification: PollNotification
    ) -> None:
        session.delete(notification)
        session.flush()


__all__ = ["NotificationRepository"]
