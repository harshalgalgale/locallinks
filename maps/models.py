from django.db import models
from tinymce.models import HTMLField
import json
import urllib2
import re

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
	
class Type(models.Model):
	title = models.CharField(max_length=64)
	description = models.CharField(max_length=256, blank=True)
	layer = models.ForeignKey(Layer)
	
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
	local_url = models.CharField(max_length=128)
	thumbnail = models.ImageField(upload_to='img/asset_thumbs/', blank=True)
	map = models.ForeignKey(Map)
	type = models.ForeignKey(Type)
	layer = models.ForeignKey(Layer)
	likes = models.IntegerField()
	address_1 = models.CharField(max_length=256)
	address_2 = models.CharField(max_length=256, blank=True)
	address_3 = models.CharField(max_length=256, blank=True)
	city = models.ForeignKey(City)
	postcode = models.CharField(max_length=64)
	lat = models.CharField(max_length=64)
	lon = models.CharField(max_length=64)
	phone = models.CharField(max_length=64, blank=True)
	email = models.EmailField(max_length=254, blank=True)
	url = models.URLField(blank=True)
	published = models.BooleanField()
	
	def __unicode__(self):
		return self.title
	
	def save(self, *args, **kwargs):
		self.build_local_url()
		if not self.pk:
			self.set_coords()
		super(Place, self).save(*args, **kwargs)
		
	def set_coords(self):
		"""Get the coordinates of the asset using the postcode and mapit"""
		url = 'http://mapit.mysociety.org/postcode/'+self.postcode.replace(" ", "")
		data = urllib2.urlopen(url)
		data = json.load(data)
		self.lat = data['wgs84_lat']
		self.lon = data['wgs84_lon']
	
	def build_local_url(self):
		"""Generate a machine-friendly URL"""
		self.local_url = encode_url(self.title)
	
		
class Quote(models.Model):
	place = models.ForeignKey(Place)
	text = models.CharField(max_length=512)
	
	def __unicode__(self):
		return self.text

class Person(models.Model):
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
		return self.text

class Page(models.Model):
	title = models.CharField(max_length=128)
	local_url = models.CharField(max_length=128)
	content = HTMLField()
	
	def save(self, *args, **kwargs):
		self.build_local_url()
		super(Page, self).save(*args, **kwargs)
	
	def build_local_url(self):
		"""Generate a machine-friendly URL"""
		self.page_local_url = encode_url(self.title)
	
	def __unicode__(self):
		return self.title