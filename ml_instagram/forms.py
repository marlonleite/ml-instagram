from datetime import datetime, timedelta

from django import forms
from django.conf import settings

from ml_instagram.instagram import InstagramOauthAPI
from ml_instagram.models import MLInstagram, MLInstagramSetting


class MLInstagramSettingAdminForm(forms.ModelForm):
    class Meta:
        model = MLInstagramSetting
        fields = "__all__"

    def clean_code(self):
        code = self.cleaned_data['code']
        return code.replace(
            f"{settings.ML_INSTAGRAM_REDIRECT_URI}?code=", ""
        ).replace("#_", "")


class MLInstagramAdminForm(forms.ModelForm):
    class Meta:
        model = MLInstagram
        fields = "__all__"

    def clean(self):
        client = InstagramOauthAPI()
        short_lived_access_token = self.cleaned_data.get('short_lived_access_token')
        code = self.cleaned_data.get("code")
        if code and not short_lived_access_token:
            response = client.get_short_lived_access_token(code.code)
            if "errors" in response:
                self.add_error('short_lived_access_token', response["errors"])
            else:
                self.cleaned_data["short_lived_access_token"] = response["access_token"]
                self.cleaned_data["user_id"] = response["user_id"]

        long_lived_access_token = self.cleaned_data.get('long_lived_access_token')
        if not long_lived_access_token:
            if short_lived_access_token:
                response = client.get_long_lived_access_token(short_lived_access_token)
                if "errors" in response:
                    self.add_error('long_lived_access_token', response["errors"])
                else:
                    self.cleaned_data["long_lived_access_token"] = response["access_token"]
                    self.cleaned_data["refresh_date"] = datetime.now() + timedelta(seconds=response["expires_in"])

        return self.cleaned_data
