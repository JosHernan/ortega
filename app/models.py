from __future__ import unicode_literals

from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from comments.models import Comment

class userProfile(models.Model):
	user 		=	models.OneToOneField(User)
	photo 		=	models.ImageField(upload_to="MultimediaData/Proyecto/",null=True,blank=True)
	telefono	=	models.CharField(max_length=30)
	correo= models.CharField(max_length=50)
	

	def __unicode__(self):
		return self.user.username

class Category(models.Model):
	nombre =models.CharField(max_length=100)

	def __unicode__(self):
		return self.nombre


class Casos(models.Model):
	user=models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	nombre = models.CharField(max_length=200)
	descripcion =models.TextField()
	categoria=models.ManyToManyField(Category)
	publish = models.DateField(auto_now=False, auto_now_add=False)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __unicode__(self):
		return self.nombre

	def  get_absolute_url(self):
		#return reverse("encuesta:detail")
		return "/ortega/%s/"%(self.id)



	@property 
	def comments(self):
		instance = self
		qs = Comment.objects.filter_by_instance(instance)
		return qs

	
	@property 
	def get_content_type(self):
	    instance=self
	    content_type = ContentType.objects.get_for_model(instance.__class__)
	    return content_type 





