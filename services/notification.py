"""
Short-polling notification service.

Client A dispatches notifications; client B polls /poll/status on an interval
and fetches details through /poll/notification/list.
"""

from uuid import UUID

from sqlalchemy.orm import Session

from core.enums import PollType
from core.exceptions import (
    NotificationError,
    NotificationNotFoundError,
    NotificationAccessError,
    NotificationUserError,
)
from models.polls import PollNotification
from repo.notification import NotificationRepository as notification_repo
from repo.poll import PollRepository as poll_repo
from repo.user import UserRepository as user_repo
from schemas.enums import ReturnStatus
from schemas.notifications import (
    Notification,
    NotificationAck,
    NotificationAckAction,
    NotificationList,
    SendNotification,
)
from schemas.polling import PollEntry, PollStatusRequest, PollStatusResponse


class NotificationService:
    @staticmethod
    def _resolve_user_id(profile_id: str, session: Session) -> UUID:
        user_id = user_repo.get_user_id_by_profile_id(profile_id, session)
        if not user_id:
            raise NotificationUserError()
        return user_id

    @staticmethod
    def _to_notification(record: PollNotification) -> Notification:
        return Notification(
            id=record.id,
            poll_from=record.poll_from,
            issue_time=record.issue_time,
            content=record.content,
            priority=record.priority,
            read=record.read,
        )

    @staticmethod
    def poll_status(
        request: PollStatusRequest,
        profile_id: str,
        session: Session,
    ) -> PollStatusResponse:
        try:
            user_id = NotificationService._resolve_user_id(profile_id, session)
            pending_rows = poll_repo.list_pending_for_user(
                session, user_id, request.poll_type
            )

            pending = [
                PollEntry(
                    poll_from=row.poll_from,
                    poll_type=row.poll_type,
                    poll_count=row.poll_count,
                    poll_ids=list(row.poll_id or []),
                )
                for row in pending_rows
            ]

            return PollStatusResponse(
                count=len(pending),
                status=ReturnStatus.success,
                pending=pending,
            )
        except NotificationUserError:
            session.rollback()
            raise
        except Exception:
            session.rollback()
            raise NotificationError()
        finally:
            session.close()

    @staticmethod
    def send(
        payload: SendNotification,
        profile_id: str,
        session: Session,
    ) -> Notification:
        try:
            sender_id = NotificationService._resolve_user_id(profile_id, session)

            if payload.recipient_id == sender_id:
                raise NotificationAccessError()

            record = notification_repo.create_notification(session, sender_id, payload)
            poll_repo.append_record(
                session,
                sender_id,
                payload.recipient_id,
                PollType.notification,
                record.id,
            )
            session.commit()

            return NotificationService._to_notification(record)
        except (NotificationUserError, NotificationAccessError):
            session.rollback()
            raise
        except Exception:
            session.rollback()
            raise NotificationError()
        finally:
            session.close()

    @staticmethod
    def list_notifications(
        profile_id: str,
        session: Session,
        unread_only: bool = False,
    ) -> NotificationList:
        try:
            user_id = NotificationService._resolve_user_id(profile_id, session)
            records = notification_repo.list_for_recipient(
                session, user_id, unread_only=unread_only
            )
            data = [NotificationService._to_notification(record) for record in records]

            return NotificationList(
                count=len(data),
                status=ReturnStatus.success,
                data=data,
            )
        except NotificationUserError:
            session.rollback()
            raise
        except Exception:
            session.rollback()
            raise NotificationError()
        finally:
            session.close()

    @staticmethod
    def acknowledge(
        payload: NotificationAck,
        profile_id: str,
        session: Session,
    ) -> Notification | None:
        try:
            user_id = NotificationService._resolve_user_id(profile_id, session)
            record = notification_repo.get_by_id(session, payload.notification_id)

            if not record or record.poll_to != user_id:
                raise NotificationNotFoundError()

            if payload.action in (
                NotificationAckAction.ack,
                NotificationAckAction.ack_del,
            ):
                notification_repo.mark_read(session, record)

            poll_repo.remove_record(
                session,
                record.poll_from,
                record.poll_to,
                PollType.notification,
                record.id,
            )

            if payload.action in (
                NotificationAckAction.delete,
                NotificationAckAction.ack_del,
            ):
                notification_repo.delete_notification(session, record)
                session.commit()
                return None

            session.commit()
            session.refresh(record)
            return NotificationService._to_notification(record)
        except (NotificationUserError, NotificationNotFoundError):
            session.rollback()
            raise
        except Exception:
            session.rollback()
            raise NotificationError()
        finally:
            session.close()
