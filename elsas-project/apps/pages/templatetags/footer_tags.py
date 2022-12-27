from django import template

from apps.pages.models import *

register = template.Library()

# @register.simple_tag
# def page_data():
#     output = Other.objects.all()[:1].get()
#     return output

# @register.simple_tag
# def social_menus():
#     output = Footer.objects.all()
#     return output

# @register.simple_tag
# def social_links():
#     output = FooterLink.objects.all()
#     return output

# @register.simple_tag
# def legal_links():
#     output = LegalPage.objects.filter(visible = True)
#     return output