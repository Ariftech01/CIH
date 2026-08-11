from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
from backend.risk_intelligence.schemas.automation_risk import NotificationContext
from backend.app_logging.logger import logger as app_logger

class NotificationEngine:
    """
    Enterprise Notification Engine & Communication Orchestrator.
    Manages event-driven notifications, priority assignment (CRITICAL, HIGH, MEDIUM, LOW),
    recipient routing (Project Manager, Safety Officer, Compliance Officer, Insurance Manager),
    in-app notification queues, and multi-channel delivery readiness adapters (Email, Teams, Slack, Webhooks, SMS).
    """

    def __init__(self):
        self._notifications: List[NotificationContext] = []

    def dispatch_notification(
        self,
        event_type: str,
        title: str,
        message: str,
        priority: str = "MEDIUM",
        recipients: Optional[List[str]] = None,
        channel: str = "IN_APP"
    ) -> NotificationContext:
        notif_id = f"NOTIF_{uuid.uuid4().hex[:8]}"

        default_recipients = recipients or self._resolve_recipients(event_type, priority)

        context = NotificationContext(
            notification_id=notif_id,
            event_type=event_type,
            priority=priority,
            recipients=default_recipients,
            title=title,
            message=message,
            status="DISPATCHED",
            channel=channel,
            timestamp=datetime.utcnow()
        )

        self._notifications.append(context)
        app_logger.info(f"NotificationEngine dispatched notification '{notif_id}' ({priority}) to {default_recipients}: '{title}'")
        return context

    def _resolve_recipients(self, event_type: str, priority: str) -> List[str]:
        """Resolves target recipient roles based on event category and severity priority."""
        recipients = ["Project Manager"]
        if "SAFETY" in event_type.upper() or priority in ["CRITICAL", "HIGH"]:
            recipients.append("Safety Officer")
        if "COMPLIANCE" in event_type.upper() or priority in ["CRITICAL", "HIGH"]:
            recipients.append("Compliance Officer")
        if "INSURANCE" in event_type.upper():
            recipients.append("Insurance Manager")
        if priority == "CRITICAL":
            recipients.append("Executive Team")
        return recipients

    def get_notifications(self, recipient: Optional[str] = None, limit: int = 10) -> List[NotificationContext]:
        if recipient:
            filtered = [n for n in self._notifications if recipient in n.recipients]
            return filtered[-limit:]
        return self._notifications[-limit:]

    # --- Extension Interfaces for Future Multi-Channel Delivery Ecosystems ---

    def dispatch_email_notification(self, context: NotificationContext, email_address: str) -> Dict[str, Any]:
        """Extension point for SMTP / SendGrid Email delivery."""
        return {"notification_id": context.notification_id, "channel": "EMAIL", "to": email_address, "status": "READY_FOR_DELIVERY"}

    def dispatch_teams_notification(self, context: NotificationContext, webhook_url: str) -> Dict[str, Any]:
        """Extension point for Microsoft Teams Webhook delivery."""
        return {"notification_id": context.notification_id, "channel": "TEAMS", "webhook": webhook_url, "status": "READY_FOR_DELIVERY"}

    def dispatch_slack_notification(self, context: NotificationContext, channel_name: str) -> Dict[str, Any]:
        """Extension point for Slack Webhook / App delivery."""
        return {"notification_id": context.notification_id, "channel": "SLACK", "slack_channel": channel_name, "status": "READY_FOR_DELIVERY"}

notification_engine = NotificationEngine()
