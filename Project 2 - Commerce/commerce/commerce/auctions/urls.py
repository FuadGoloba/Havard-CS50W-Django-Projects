from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name='createlisting'),
    path("item=<int:listing_id>", views.item_detail, name='item_detail'),
    path("close_bid/item=<int:listing_id>", views.close_bid, name='close_bid'),
    path("add_comment/item=<int:listing_id>", views.add_comment, name='add_comment'),
    path("closed_listing", views.closed_listing, name='closed_listing'),
    path("add_watchlist/item=<int:listing_id>", views.add_watchlist, name='add_watchlist'),
    path("remove_watchlist/item=<int:listing_id>", views.remove_watchlist, name='remove_watchlist'),
    path("watchlist", views.view_watchlist, name='view_watchlist'),
    path("categories", views.categories, name='categories'),
    path("category=<int:category_id>", views.category_listing, name='category_listing')
]
