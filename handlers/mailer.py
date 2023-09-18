from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import TemplateDoesNotExist, render_to_string
from django.utils.html import strip_tags


# this module is to help us in sending email
# without having to write lots of send_mail functions to a 
# view of a class in our main
# views

class TemplateEmail:
    def __init__(self, to, subject, template, context={}, from_email=None, sub_folder='', reply_to=None, **email_kwargs):
        self.to=to
        self.subject=subject
        self.template=template
        self.context=context
        self.from_emil=from_email or settings.DEFAULT_FROM_EMAIL
        self.reply_to=reply_to

        # subfolder for the email template 
        # this is not required,, nesting can only be done
        # one subfolder deep
        # will figure out how to improve it for deeper nesting
        self.sub_folder = sub_folder
        
        # check if 'template' in context and extract it

        self.context['template'] = template
        # obtain a tuple of html, plain text content
        self.html_content, self.plain_content = self.render_content()
        
        # check the type of to address and the reply and the convert them to list as appropriiate
        
        self.to = self.to if not isinstance(self.to, str) else [self.to]
        if self.reply_to:
            self.reply_to = (
                self.reply_to if not isinstance(self.reply_to, str) else [self.reply_to]
            )
        self.django_email = EmailMultiAlternatives(
            subject=self.subject,
            body=self.plain_content,
            from_email=self.from_emil,
            to=self.to,
            reply_to=self.reply_to,
            **email_kwargs
        )
        
        self.django_email.attach_alternative(self.html_content, "text/html")

    def render_content(self):
        html_content = self.render_html()
        try:
            plain_content = self.render_plain()
        except TemplateDoesNotExist:
            plain_content = strip_tags(html_content)
        return html_content, plain_content

    
    def render_html(self):
        return render_to_string(self.get_html_template_name(), self.context)
    
    def render_plain(self):
        return render_to_string(self.get_plain_template_name(), self.context)
    
    def get_sub_folter_template_name(self):
        return self.sub_folder
    
    
    def get_html_template_name(self):
        return "{folder}/{sub_folder}{file}.html".format(
            folder="email", sub_folder=self.get_sub_folter_template_name(), file=self.template
            )
    
    def get_plain_template_name(self):
        return "{folder}/{sub_folder}/{file}.txt".format(
            folder="email",sub_folder=self.get_sub_folter_template_name(), file=self.template
            )
    
    # after instanciation we can just call the send 
    def send(self, **email_content):
        return self.django_email.send(**email_content)



