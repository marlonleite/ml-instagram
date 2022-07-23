from datetime import date, timedelta, datetime

from django.template import Library

from ml_instagram.instagram import InstagramOauthAPI
from ml_instagram.models import MLInstagram

register = Library()


@register.simple_tag()
def my_feeds(limit=12):
    feeds = []
    instagram = MLInstagram.objects.first()
    if instagram:
        today = date.today()
        client = InstagramOauthAPI()
        if today > instagram.refresh_date.date():
            response = client.refresh_access_token(instagram.long_lived_access_token)
            if "errors" in response:
                return []
            instagram.long_lived_access_token = response["access_token"]
            instagram.refresh_date = datetime.now() + timedelta(seconds=response["expires_in"])
            instagram.save()

        new_feeds = client.get_media(instagram.long_lived_access_token)[:limit]
        feeds.extend(new_feeds)
    return feeds
