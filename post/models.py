from django.db import models

# Create your models here.

class Post(models.Model):
	"""docstring for Post"""
	""" Post """
	title 	= models.CharField(max_length=30)
	content = models.TextField()
	read = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)
	updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
	created_date = models.DateTimeField(auto_now_add=True, auto_now=False)
	
	def __str__(self):
		return self.title

class Comment(models.Model):
	"""docstring for Post"""
	""" Post """
	post = models.ForeignKey('Post', on_delete=models.CASCADE)
	name = models.CharField(max_length=50, null=True)
	comment = models.TextField()
	likes = models.IntegerField(default=0)
	created_date = models.DateTimeField(auto_now_add=True, auto_now=False)
	
	def __str__(self):
		return self.post