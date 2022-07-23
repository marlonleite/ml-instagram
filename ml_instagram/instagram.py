import logging

import requests
from django.conf import settings

LOGGER = logging.getLogger(__name__)


class InstagramOauthAPI:
    instagram_oauth_url = "https://api.instagram.com/oauth"
    instagram_graph_url = "https://graph.instagram.com"

    def __init__(self):
        self.client_id = settings.ML_INSTAGRAM_CLIENT_ID
        self.client_secret = settings.ML_INSTAGRAM_CLIENT_SECRET
        self.redirect_uri = settings.ML_INSTAGRAM_REDIRECT_URI

    def authorize_url(self):
        url = f"{self.instagram_oauth_url}/authorize"
        url += f"?client_id={self.client_id}&redirect_uri={self.redirect_uri}"
        url += "&scope=user_profile,user_media&response_type=code"
        return {"url": url}

    def get_short_lived_access_token(self, code):
        """
        By default, Instagram User Access Tokens are short-lived
        and are valid for one hour.
        However, short-lived tokens can be exchanged for
        long-lived tokens.
        """
        url = f"{self.instagram_oauth_url}/access_token"

        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri,
            "code": code,
        }

        response = requests.post(url, data=data)

        if response.ok:
            return response.json()

        LOGGER.warning(
            "Short_lived_access_token error: response=%s",
            response.text,
        )
        return {"errors": response.text}

    def get_long_lived_access_token(self, short_lived_access_token):
        """
        https://developers.facebook.com/docs/instagram-basic-display-api/guides/long-lived-access-tokens
        Long-lived tokens are valid for 60 days and can be refreshed as
        long as they are at least 24 hours old but have not expired
        """
        url = f"{self.instagram_graph_url}/access_token"
        params = {
            "grant_type": "ig_exchange_token",
            "client_secret": self.client_secret,
            "access_token": short_lived_access_token,
        }
        response = requests.get(url, params=params)

        if response.ok:
            return response.json()

        LOGGER.warning(
            "Long_lived_access_token error: response=%s",
            response.text,
        )
        return {"errors": response.text}

    def refresh_access_token(self, long_lived_access_token):
        url = f"{self.instagram_graph_url}/refresh_access_token"
        params = {
            "grant_type": "ig_refresh_token",
            "access_token": long_lived_access_token,
        }
        response = requests.get(url, params=params)
        if response.ok:
            return response.json()

        LOGGER.warning(
            "refresh_access_token error: response=%s",
            response.text,
        )
        return {"errors": response.text}

    def get_media(self, long_lived_access_token):
        url = f"{self.instagram_graph_url}/me/media"
        params = {
            "fields": "id,caption,permalink,media_url,thumbnail_url,media_type"
        }
        headers = {
            "Authorization": f"Bearer {long_lived_access_token}"
        }
        response = requests.get(url, params=params, headers=headers)
        if response.ok:
            return response.json().get("data")

        LOGGER.warning(
            "get_media error: response=%s",
            response.text,
        )
        return []

    def get_oembed(self, access_token):
        url = f"{self.instagram_graph_url}/instagram_oembed"
        data = {
            "access_token": access_token,
        }
        response = requests.get(url, params=data)
        if response.ok:
            return response.json().get("data")
        return []
