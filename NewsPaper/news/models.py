from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse
from django.core.cache import cache



class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rate = models.IntegerField(default=0)

    def __str__(self):
        return str(self.author)


    def update_rating(self):
        post_rate = self.post_set.aggregate(postRating=Sum("news_rate"))
        p_r = 0
        p_r += post_rate.get("postRating")

        comment_rate = self.author.comment_set.aggregate(commentRating=Sum("comment_rate"))
        c_r = 0
        c_r += comment_rate.get("commentRating")

        self.author_rate = p_r * 3 + c_r
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return str(self.category_name)


class Post(models.Model):
    article = 'AR'
    news = 'NE'

    NEWSTYPES = [
        (article, 'Article'),
        (news, 'News'),
    ]

    choice = models.CharField(max_length=2,
                              choices=NEWSTYPES,
                              default=news)

    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    content = models.TextField(default="No News / Articles Yet")
    news_rate = models.IntegerField(default=0)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')

    def preview(self):
        return f"{self.content[0:123]}..."

    def like(self):
        self.news_rate += 1
        self.save()

    def dislike(self):
        self.news_rate -= 1
        self.save()

    def __str__(self):
        return f'{self.title.title()}: {self.content[:100]}'

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'news_article-{self.pk}')

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_content = models.TextField(default="No Comments Yet")
    date = models.DateTimeField(auto_now_add=True)
    comment_rate = models.IntegerField(default=0)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentator = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.comment_rate += 1
        self.save()

    def dislike(self):
        self.comment_rate -= 1
        self.save()
