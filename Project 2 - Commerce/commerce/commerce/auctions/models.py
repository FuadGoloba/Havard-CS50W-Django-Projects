from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionStatus(models.Model):
    name = models.CharField(max_length=6)

    def __str__(self):
        return f"{self.name}"


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    listing_price = models.DecimalField(max_digits=6, decimal_places=2)
    listing_date = models.DateTimeField(auto_now=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_listings')
    status = models.ForeignKey(AuctionStatus, on_delete=models.CASCADE)
    image = models.URLField()

    def __str__(self):
        #return f"{self.id} {self.title} {self.description} {self.category} {self.listing_price} {self.listing_date} {self.seller.id} {self.status} {self.image}"  
        return f"{self.title}"

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    bid_price = models.DecimalField(max_digits=6, decimal_places=2)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="biddings")
    bid_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bidder} {self.bid_price} {self.listing.title} {self.bid_date}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} {self.listing}"
    

class Comment(models.Model):
    comment = models.TextField()
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    comment_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f" {self.reviewer} {self.comment} {self.comment_date}"
    