from django.conf import settings
from django.core.mail import send_mail, send_mass_mail, get_connection, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.translation import ugettext

from .base import BaseBackend


def send_mass_html_mail(datatuple, fail_silently=False, user=None, password=None, connection=None):
    connection = connection or get_connection(username=user, password=password, fail_silently=fail_silently)
    messages = []
    for subject, html, from_email, recipient in datatuple:
        message = EmailMultiAlternatives(subject, '', from_email, recipient)
        message.attach_alternative(html, 'text/html')
        messages.append(message)
    return connection.send_messages(messages)


class EmailBackend(BaseBackend):
    spam_sensitivity = 2
    BULK_DELIVERY = True

    def can_send(self, user, notice_type, scoping):
        can_send = super(EmailBackend, self).can_send(user, notice_type, scoping)
        if can_send and user.email:
            return True
        return False

    def get_datatuple(self, recipient, sender, notice_type, extra_context):
        # TODO: require this to be passed in extra_context

        context = self.default_context()
        context.update({
            "recipient": recipient,
            "sender": sender,
            "notice": ugettext(notice_type.display),
        })
        context.update(extra_context)

        message_type = "txt" if not settings.PINAX_NOTIFICATIONS_USE_HTML_EMAIL else "html"

        email_body_template = "pinax/notifications/email_body.{0}".format(message_type)
        full_template = "full.{0}".format(message_type)

        messages = self.get_formatted_messages((
            "short.txt",
            full_template
        ), notice_type.label, context)

        #Subject
        context.update({"message": messages["short.txt"]})
        subject = "".join(render_to_string("pinax/notifications/email_subject.txt", context).splitlines())

        #Body
        context.update({"message": messages[full_template]})
        body = render_to_string(email_body_template, context)

        return subject, body, settings.DEFAULT_FROM_EMAIL, [recipient.email]


    def deliver(self, recipient, sender, notice_type, extra_context):
        subject, body, from_email, recipient_list = self.get_datatuple(recipient, sender, notice_type, extra_context)

        if settings.PINAX_NOTIFICATIONS_USE_HTML_EMAIL:
            send_mail(subject, "", from_email, recipient_list, html_message=body)
        else:
            send_mail(subject, body, from_email, recipient_list)

    def bulk_deliver(self, messages):
        send_mass_html_mail(tuple(messages))
