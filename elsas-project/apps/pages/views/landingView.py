from django.db.models import Q

from django.views.generic import (
	TemplateView,
)

from apps.pages.models import *


# Create your views here

class LandingView(TemplateView):
    template_name = 'landing.html'

    # def get_context_data(self, **kwargs):

    #     context = super(LandingView, self).get_context_data(**kwargs)

    #     context['page'] = Page.objects.get(type_about = 'art')
    #     context['teamcategories'] = TeamCategory.objects.filter(about_pages__type_about = 'art')
    #     context['qa_page'] = QA.objects.all()[0]
    #     context['qas'] = Question.objects.all()

    #     all_images = QAImage.objects.all().order_by('location')
    #     for image in all_images:
    #             context[image.location] = image
        
    #     return context
