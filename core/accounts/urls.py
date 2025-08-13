from django.urls import path
from .views import user_lists, user_profile, profiledetail


urlpatterns = [
    path("api/user/list/", user_lists, name="list-user"),
    path("api/user/you/", user_profile, name="profile-view"),
    path("spi/profile/detail/", profiledetail , name="profile-detail")

]
