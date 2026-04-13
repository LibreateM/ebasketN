# eapp/email_backend.py
import ssl
from django.core.mail.backends.smtp import EmailBackend


class CustomEmailBackend(EmailBackend):
    def open(self):
        if self.connection:
            return False
        
        # SSL verification bypass for development
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        self.connection = self.connection_class(
            self.host, self.port,
            timeout=self.timeout,
        )
        self.connection.ehlo()
        if self.use_tls:
            self.connection.starttls(context=ssl_context)
            self.connection.ehlo()
        if self.username and self.password:
            self.connection.login(self.username, self.password)
        return True