from django.db import models
from django.utils import timezone

from ml_instagram.instagram import InstagramOauthAPI


class MLInstagramSetting(models.Model):
    code = models.TextField(blank=True)

    class Meta:
        db_table = "ml_instagram_setting"

    def __str__(self):
        return f"{self.code[:25]} ..."

    @property
    def authorize_url(self):
        client = InstagramOauthAPI()
        return client.authorize_url()["url"]

    def get_code(self):
        return str(self.code)


class MLInstagram(models.Model):
    code = models.ForeignKey(MLInstagramSetting, on_delete=models.CASCADE)
    refresh_date = models.DateTimeField(default=timezone.now)
    short_lived_access_token = models.TextField(blank=True)
    long_lived_access_token = models.TextField(blank=True)
    user_id = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = "ml_instagram"

    def __str__(self):
        return self.user_id


    # def save(self, *args, **kwargs):
    #     if not self.short_lived_access_token:
    #         client = InstagramOauthAPI()
    #         response = client.get_short_lived_access_token(self.code.get_code())
    #
    #         if not response.get("error"):
    #             self.short_lived_access_token = str(response["access_token"])
    #             self.user_id = str(response["user_id"])
    #
    #     if not self.long_lived_access_token:
    #         if self.short_lived_access_token:
    #             client = InstagramOauthAPI()
    #             response = client.get_long_lived_access_token(self.short_lived_access_token)
    #
    #             if not response.get("error"):
    #                 self.long_lived_access_token = str(response["access_token"])
    #
    #     super().save(*args, **kwargs)
