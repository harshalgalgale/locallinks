from django.db import models
from tinymce.models import HTMLField
from image_cropping import ImageRatioField
import json
import urllib2
import re
from taggit.managers import TaggableManager

def encode_url(str):
	return re.sub('[^A-Za-z0-9]+', '_', str)

class Map(models.Model):
	title = models.CharField(max_length=64)
	lon = models.CharField(max_length=64)
	lat = models.CharField(max_length=64)
	
	def __unicode__(self):
		return self.title

class Layer(models.Model):
	title = models.CharField(max_length=128)
	description = models.CharField(max_length=256, blank=True)
	
	def __unicode__(self):  
	    return self.title
	
class City(models.Model):
	title = models.CharField(max_length=64)
	def __unicode__(self):
		return self.title
	
	class Meta:
		verbose_name_plural = "Cities"

class Place(models.Model):
	title = models.CharField(max_length=128)
	local_url = models.SlugField()
	thumbnail = models.ImageField(upload_to='img/asset_thumbs/', blank=True)
	cropping = ImageRatioField('thumbnail', '64x64')
	map = models.ForeignKey(Map)
	"""type = models.ForeignKey(Type)"""
	layer = models.ForeignKey(Layer)
	likes = models.IntegerField(default=0)
	address_1 = models.CharField(max_length=256)
	address_2 = models.CharField(max_length=256, blank=True)
	address_3 = models.CharField(max_length=256, blank=True)
	city = models.ForeignKey(City)
	postcode = models.CharField(max_length=64)
	lat = models.CharField(max_length=64)
	lon = models.CharField(max_length=64)
	phone = models.CharField(max_length=64, blank=True)
	email = models.EmailField(max_length=254, blank=True)
	url = models.URLField('URL', blank=True)
	directory_url = models.URLField('Idea Store Directory URL', blank=True)
	published = models.BooleanField()
	description = models.CharField(max_length=512, blank=True)
	tags = TaggableManager()
	
	def __unicode__(self):
		return self.title
	
	def save(self, *args, **kwargs):
		self.set_coords()
		super(Place, self).save(*args, **kwargs)
		
	def set_coords(self):
		"""Address lookup using Google Maps"""
		
		address = [self.address_1, self.address_2, self.address_3, self.postcode]
		url = ''
		for i in address:
			if i != '':
				url = url+',+'+i.replace(" ", "+")
		url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+url[2:]+',+London,+UK&sensor=true_or_false'
		data = urllib2.urlopen(url)
		data = json.load(data)
		self.lat = data['results'][0]['geometry']['location']['lat']
		self.lon = data['results'][0]['geometry']['location']['lng']
	
		
class Quote(models.Model):
	place = models.ForeignKey(Place)
	text = models.CharField(max_length=512)
	
	def __unicode__(self):
		return self.text

class Activity(models.Model):
	place = models.ForeignKey(Place)
	title = models.CharField(max_length=128)
	description = models.CharField(max_length=512, blank=True)
	
	def __unicode__(self):
		return self.title
	
	class Meta:
		verbose_name_plural = "Activities"

class ActivityQuote(models.Model):
	place = models.ForeignKey(Place)
	activity = models.ForeignKey(Activity)
	text = models.CharField(max_length=512)

	def __unicode__(self):
		return self.text

"""class Person(models.Model):
	first_name = models.CharField(max_length=128)
	last_name = models.CharField(max_length=128)
	avatar = models.ImageField(upload_to='img/avatars/', blank=True)
	bio = models.CharField(max_length=512)
	
	def __unicode__(self):
		return self.first_name + ' ' + self.last_name
	
	class Meta:
		verbose_name_plural = "People"

class Role(models.Model):
	person = models.ForeignKey(Person)
	place = models.ForeignKey(Place)
	text = models.CharField(max_length=512)
	
	def __unicode__(self):
		return self.text"""

class Photo(models.Model):
	place = models.ForeignKey(Place)
	photo = models.ImageField(upload_to='img/asset_photos/', blank=True)
	cropping = ImageRatioField('thumbnail', '64x64')
	alt = models.CharField(max_length=64, blank=True)
	credit = models.CharField(max_length=128, blank=True)
	
	def __unicode__(self):
		return self.alt

class Page(models.Model):
	title = models.CharField(max_length=128)
	local_url = models.SlugField()
	content = HTMLField()
	
	def __unicode__(self):
		return self.title