from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("watchlist/add/<int:listing_id>/", views.watchlist_add_item, name="watchlist_add"),
    path("watchlist/remove/<int:listing_id>/", views.watchlist_remove_item, name="watchlist_remove"),
    path("listing/add/", views.add_listing, name="add_listing"),
    path("listing/<int:listing_id>/", views.listing_detail, name="listing_detail"),
]
