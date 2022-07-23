from datetime import datetime, timedelta

from django.contrib import admin
from django.utils.html import format_html
from django.contrib import messages
from ml_instagram.forms import MLInstagramAdminForm, MLInstagramSettingAdminForm
from ml_instagram.instagram import InstagramOauthAPI
from ml_instagram.models import MLInstagramSetting, MLInstagram


@admin.register(MLInstagramSetting)
class MLInstagramSettingAdmin(admin.ModelAdmin):
    list_display = ["code"]
    readonly_fields = ["show_authorize_url"]
    form = MLInstagramSettingAdminForm

    def show_authorize_url(self, obj):
        return format_html(
            '<a target="_blank" href="{url}">Authorize Url</a>', url=obj.authorize_url
        )

    show_authorize_url.allow_tags = True


@admin.register(MLInstagram)
class MLInstagramAdmin(admin.ModelAdmin):
    list_display = ["user_id", "refresh_date"]
    form = MLInstagramAdminForm
    actions = ['refresh_token']

    def refresh_token(self, request, queryset):
        for obj in queryset:
            client = InstagramOauthAPI()
            response = client.refresh_access_token(obj.long_lived_access_token)
            if "errors" in response:
                self.message_user(request, f'{response["errors"]}', messages.ERROR)
            else:
                obj.long_lived_access_token = response["access_token"]
                obj.refresh_date = datetime.now() + timedelta(seconds=response["expires_in"])
                obj.save()
                self.message_user(request, "long_lived_access_token atualizado com sucesso", messages.SUCCESS)

    refresh_token.short_description = "Atualizar Long Lived Access Token"
