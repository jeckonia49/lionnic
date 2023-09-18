from .forms import SubscriptionForm


def get_subscription_processors(request):
    return dict(
        subscriber_form=SubscriptionForm()
    )
