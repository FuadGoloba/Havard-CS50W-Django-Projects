from django.contrib import admin

from .models import User, AuctionListing, Bid, AuctionStatus, Comment, Category, Watchlist
# Register your models here.

class AuctionListingAdmin(admin.ModelAdmin):
     list_display = ['title', 'description', 'category', 'listing_price', 'listing_date', 'seller', 'status','image']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

class BidAdmin(admin.ModelAdmin):
    list_display = ['bidder', 'bid_price', 'listing', 'bid_date']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['reviewer', 'listing', 'comment', "comment_date"]

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'listing']

admin.site.register(User)
admin.site.register(AuctionStatus)
admin.site.register(AuctionListing, AuctionListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Watchlist, WatchlistAdmin)