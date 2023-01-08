from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    _rating = models.IntegerField(default=0, db_column='rating')

    def update_rating(self):
        sum_posts_rating = self.post_set.all().aggregate(
            Sum('post_rating'))['post_rating__sum']*3
        sum_comments = self.id_user.comment_set.all().aggregate(
            Sum('comment_rating'))['comment_rating__sum']
        sum_comments_post = self.post_set.all().aggregate(
            Sum('comment__comment_rating'))['comment__comment_rating__sum']
        self.rating = sum_posts_rating + sum_comments + sum_comments_post
        self.save()

    def __str__(self) -> str:
        return f'{self.user}'


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self) -> str:
        return f'{self.name}'


news = 'NE'
article = 'AR'
TYPE_CATEGORY = [
    (news, 'Новость'),
    (article, 'Статья'),
]


class Post(models.Model):
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    type_post = models.CharField(
        max_length=2,
        choices=TYPE_CATEGORY
    )
    date = models.DateField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=64)
    text = models.TextField(max_length=1000)
    _rating = models.IntegerField(default=0, db_column='rating')

    def like(self):
        self._rating += 1

    def dislike(self):
        self._rating -= 1

    def preview(self):
        return f'{self.text[:124]}...'


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateField(auto_now_add=True)
    _rating = models.IntegerField(default=0, db_column='rating')

    def like(self):
        self._rating += 1

    def dislike(self):
        self._rating -= 1
