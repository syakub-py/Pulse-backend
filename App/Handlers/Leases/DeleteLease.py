from App.DB.Models.Chat import Chat
from App.DB.Models.ChatParticipant import ChatParticipant
from App.DB.Models.PropertyLease import PropertyLease
from App.DB.Models.User import User
from App.DB.Session import session_scope as session
from App.DB.Models.Lease import Lease
from App.DB.Models.TenantLease import TenantLease
from typing import Dict, Any
from sqlalchemy import delete, select
from App.LoggerConfig import pulse_logger as logger


def deleteLease(leaseId: int) -> Dict[str, Any]:
    logger.info(f"Deleting lease: {leaseId}")
    if not leaseId:
        logger.error("No leaseId provided")
        return {"message": "Lease not found", "status_code": 500}

    try:
        with session() as db_session:
            lease_id_stmt = select(Lease).where(Lease.lease_id == leaseId)
            lease_id = db_session.execute(lease_id_stmt)

            if lease_id.rowcount == 0:
                return {"message": "Lease not found", "status_code": 404}

            tenant_query = select(TenantLease.tenant_id).where(TenantLease.lease_id == leaseId)
            tenant_id = db_session.execute(tenant_query).scalar()

            pulse_ai_user_query = select(User.user_id).where(User.name == "Pulse AI")
            pulse_ai_user_id = db_session.execute(pulse_ai_user_query).scalar()

            chat_participant_delete_stmt = (
                delete(ChatParticipant)
                .where(ChatParticipant.chat_id.in_(
                    select(Chat.chat_id)
                    .where(ChatParticipant.user_id == tenant_id)
                    .where(Chat.chat_id.notin_(
                        select(ChatParticipant.chat_id)
                        .where(ChatParticipant.user_id == pulse_ai_user_id)
                    ))
                ))
            )
            db_session.execute(chat_participant_delete_stmt)
            db_session.flush()

            chat_delete_stmt = (
                delete(Chat)
                .where(Chat.chat_id.in_(
                    select(ChatParticipant.chat_id)
                    .where(ChatParticipant.user_id == tenant_id)
                    .where(Chat.chat_id.notin_(
                        select(ChatParticipant.chat_id)
                        .where(ChatParticipant.user_id == pulse_ai_user_id)
                    ))
                ))
            )
            db_session.execute(chat_delete_stmt)
            db_session.flush()

            tenant_leases_delete_stmt = delete(TenantLease).where(TenantLease.lease_id == leaseId)
            db_session.execute(tenant_leases_delete_stmt)
            db_session.flush()

            property_lease_delete_stmt = delete(PropertyLease).where(PropertyLease.lease_id == leaseId)
            db_session.execute(property_lease_delete_stmt)
            db_session.flush()

            lease_delete_stmt = delete(Lease).where(Lease.lease_id == leaseId)
            db_session.execute(lease_delete_stmt)
            db_session.flush()

            db_session.commit()

            logger.info(f"Lease and associated tenants deleted successfully: {leaseId}")
            return {"message": "deleted lease successfully", "status_code": 200}

    except Exception as e:
        db_session.rollback()
        logger.error(f"Unexpected error deleting a lease: {str(e)}")
        return {"message": "error deleting lease: " + str(e), "status_code": 500}
    finally:
        db_session.close()
