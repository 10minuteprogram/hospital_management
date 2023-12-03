from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from email.utils import formataddr
from django.conf import settings

def send_email(subject, to_email, template_name, context, file_paths):
    try:
        # Render the HTML template with context
        html_template = render_to_string(template_name, context)

        from_email = settings.EMAIL_HOST_USER
        formatted_from = formataddr(('10 Minute Program', from_email))

        # Create the email message
        email = EmailMultiAlternatives(
            subject=subject,
            body="",
            from_email=formatted_from,
            to=to_email
        )

        # Attach the HTML content
        email.attach_alternative(html_template, "text/html")

        # Attach files
        for file_path in file_paths:
            email.attach_file(file_path)

        # Send the email
        email.send()
        
        return {
            "status": "sent",
            "message": "Email sent successfully"
        }
    except Exception as e:
        return {
            "status": "failed",
            "message": str(e)
        }