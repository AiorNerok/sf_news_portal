from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    _rating = models.IntegerField(default=0, db_column="rating")

    def update_rating(self):
        sum_posts_rating = (
            self.post_set.all().aggregate(Sum("_rating"))["_rating__sum"] * 3
        )
        sum_comments = self.user.comment_set.all().aggregate(Sum("_rating"))[
            "_rating__sum"
        ]
        sum_comments_post = self.post_set.all().aggregate(Sum("comment___rating"))[
            "comment___rating__sum"
        ]
        self._rating = sum_posts_rating + sum_comments + sum_comments_post
        print(self._rating)
        self.save()

    def __str__(self) -> str:
        return f"{self.user}"


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self) -> str:
        return f"{self.name}"


news = "NE"
article = "AR"
TYPE_CATEGORY = [
    (news, "Новость"),
    (article, "Статья"),
]


class Post(models.Model):
    author = models.ForeignKey("Author", on_delete=models.CASCADE)
    type_post = models.CharField(max_length=2, choices=TYPE_CATEGORY)
    date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through="PostCategory")
    title = models.CharField(max_length=64)
    text = models.TextField(max_length=1000)
    _rating = models.IntegerField(default=0, db_column="rating")

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        self._rating = int(value) if value >= 0 else 0
        self.save()

    def like(self):
        self._rating += 1
        self.save()

    def dislike(self):
        self._rating -= 1
        self.save()

    def preview(self):
        return f"{self.text[:124]}..."

    def __str__(self) -> str:
        return f"{self.author}| {self.type_post} |{self.title}"


class PostCategory(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.post}| {self.category}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateField(auto_now_add=True)
    _rating = models.IntegerField(default=0, db_column="rating")

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        self._rating = int(value) if value >= 0 else 0
        self.save()

    def like(self):
        self._rating += 1
        self.save()

    def dislike(self):
        self._rating -= 1
        self.save()

    def __str__(self) -> str:
        return f"{self.user}| {self.post}"
