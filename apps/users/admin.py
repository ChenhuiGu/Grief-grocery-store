from django.contrib import admin

from apps.users.models import *

admin.site.register([User,Address])
