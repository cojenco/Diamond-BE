from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .models import StatusUpdate
from .models import Subscription
from .models import USstate


# Register your models here.
admin.site.register(User)
admin.site.register(StatusUpdate)
admin.site.register(Subscription)
admin.site.register(USstate)