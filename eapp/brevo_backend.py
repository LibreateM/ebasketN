import requests
import json
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend

class BrevoEmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        sent = 0
        for message in email_messages:
            try:
                payload = {
                    "sender": {
                        "email": settings.DEFAULT_FROM_EMAIL
                    },
                    "to": [{"email": addr} for addr in message.to],
                    "subject": message.subject,
                    "textContent": message.body,
                }
                
                # HTML content bhi ho to add karein
                if hasattr(message, 'alternatives'):
                    for content, mimetype in message.alternatives:
                        if mimetype == 'text/html':
                            payload['htmlContent'] = content

                response = requests.post(
                    "https://api.brevo.com/v3/smtp/email",
                    headers={
                        "api-key": settings.BREVO_API_KEY,
                        "Content-Type": "application/json"
                    },
                    json=payload,
                    timeout=15
                )
                
                if response.status_code == 201:
                    sent += 1
                    
            except Exception as e:
                if not self.fail_silently:
                    raise
        return sent