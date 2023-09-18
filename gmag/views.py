from category.models import Category, SubCategory, Topic, Tag
from django.http import JsonResponse
from django.views import generic
from django.views.generic import View
from posts.models import Post
from pages.forms.forms import ContactForm
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.decorators import method_decorator
from subscriptions.forms import SubscriptionForm
from django.contrib import messages
from subscriptions.models import Subscriber
from django.http import HttpResponseRedirect


class CategoryListView(generic.TemplateView):
    template_name = "pages/category.html"


class AboutUs(generic.TemplateView):
    template_name = "pages/about.html"


class ContactUs(generic.TemplateView):
    template_name = "pages/contact.html"

    def get_context_data(self, **kwargs):
        context = super(ContactUs, self).get_context_data(**kwargs)
        context["contact_form"] = ContactForm()
        return context

    @method_decorator(csrf_exempt)
    def post(self, *args, **kwargs):
        form = ContactForm(self.request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "Your Comment Was posted successfully"})
        return JsonResponse({"message": "Something went wrong"})


class Privacy(generic.TemplateView):
    template_name = "pages/privacy.html"


class TermsCondition(generic.TemplateView):
    template_name = "pages/terms-and-condition.html"


class SubscriptionView(View):
    form_class = SubscriptionForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # check if already subscribed
            subscriber = Subscriber.objects.filter(
                email=form.cleaned_data.get("email"))
            if subscriber.exists():
                messages.info(request, "Your are already subscribed. Thanks!")
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            form.save()
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
