from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    profile_picture = models.ImageField(default="default_profile_pic.png")
    #pass


# Model for a Post
class Post(models.Model):
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts") # related_name 'posts' (User.posts) will return all the posts made by that user
    content = models.CharField(max_length=500)
    liked_by = models.ManyToManyField("User", related_name="likes") # A post can have many likers and many likers can like many posts; related_name 'likes' (User.likes) will return all of the posts a user likes
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} posted '{self.content}'"

    class Meta:
        # order post by most recent
        ordering = ['-created_date']

    # get no of likes on a post
    def get_like_count(self):
        return self.liked_by.all().count()

    def serialize(self):
        return {
            'id' : self.id,
            'author' : self.author,
            'content': self.content,
            'liked_by' : [liker.username for liker in self.liked_by.all()],
            'created_date' : self.timestamp.strftime("%b %d %Y, %I:%M %p")
            }


# Model for a User Profile of followers and following
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followings") # A Profile can have followers and related_name 'followings' (User.followings) will return all the profile that the User object follows