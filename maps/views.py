from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from datetime import datetime
from maps.models import Place, Quote, Map, Layer, Page, Activity, Photo, ActivityQuote
import re
from haystack.views import basic_search

def encode_url(str):
	return re.sub('[^A-Za-z0-9]+', '_', str)
	
	
def decode_url(str):
	return str.replace('_', ' ')


def index(request):
	context = RequestContext(request)
	map = Map.objects.get(title="Tower Hamlets")
	nav = Page.objects.all()
	context_dict = {'map': map}
	layers = {}
	context_dict['nav'] = nav
	top = Place.objects.filter(likes__gt=0).order_by('-likes')[:3]
	context_dict['top'] = top
	
	for layer in Layer.objects.all():
		place_list = {}
		place_list[layer] = Place.objects.filter(layer=layer).filter(published=True)
		layers[(layer)] = place_list[layer]
		
	context_dict['layers'] = layers	
	return render_to_response('maps/index.html', context_dict, context)
	
	
def tag(request, tag):
	context = RequestContext(request)
	map = Map.objects.get(title="Tower Hamlets")
	nav = Page.objects.all()
	context_dict = {'map': map}
	layers = {}
	context_dict['nav'] = nav
	context_dict['tag'] = tag
	places = Place.objects.filter(tags__slug=tag)
	context_dict['places'] = places
	
	for layer in Layer.objects.all():
		place_list = {}
		place_list[layer] = places.filter(layer=layer).filter(published=True)
		layers[(layer)] = place_list[layer]
		
	context_dict['layers'] = layers	
	return render_to_response('maps/tag.html', context_dict, context)
	
	
def single(request, place_title_url):
	context= RequestContext(request)
	nav = Page.objects.all()
	layers = Layer.objects.all()
	context_dict = {}
	context_dict['nav'] = nav
	context_dict['layers'] = layers
	
	try:
		place = Place.objects.get(local_url=place_title_url)
		quotes = Quote.objects.filter(place=place)
		activities = {}

		for activity in Activity.objects.filter(place=place):
			activityquotes = {}
			activityquotes[str(activity)] = ActivityQuote.objects.filter(activity=activity)
			activities[(activity)] = activityquotes[str(activity)]
		
		photos = Photo.objects.filter(place=place)
		layer = Layer.objects.get(place=place)
		similar = place.tags.similar_objects()
		tags = place.tags.names()
		context_dict['quotes'] = quotes
		context_dict['place'] = place
		context_dict['activities'] = activities
		context_dict['photos'] = photos
		context_dict['layer'] = layer
		context_dict['similar'] = similar
		context_dict['tags'] = tags
		
		if request.session.get(str(place.id)+'_has_liked'):
			has_liked = True
		
		else: 
			has_liked = False
			
		context_dict['has_liked'] = has_liked
			
	except place.DoesNotExist:
		pass
	
	return render_to_response('maps/single.html', context_dict, context)


def place(request, place_title_url):
	context = RequestContext(request)
	context_dict = {}
	
	try:
		place = Place.objects.get(local_url=place_title_url)
		quotes = Quote.objects.filter(place=place)
		activities = {}

		for activity in Activity.objects.filter(place=place):
			activityquotes = {}
			activityquotes[(activity)] = ActivityQuote.objects.filter(activity=activity)
			activities[(activity)] = activityquotes[(activity)]
		
		photos = Photo.objects.filter(place=place)
		layer = Layer.objects.get(place=place)
		similar = place.tags.similar_objects()
		tags = place.tags.names()
		context_dict['quotes'] = quotes
		context_dict['place'] = place
		context_dict['activities'] = activities
		context_dict['photos'] = photos
		context_dict['layer'] = layer
		context_dict['similar'] = similar
		context_dict['tags'] = tags
		
		if request.session.get(str(place.id)+'_has_liked'):
			has_liked = True
		
		else: 
			has_liked = False
			
		context_dict['has_liked'] = has_liked
			
	except place.DoesNotExist:
		pass
	
	return render_to_response('maps/place.html', context_dict, context)


def like_place(request):	
	context = RequestContext(request)
	place_id = None
	if request.method == 'GET':
		place_id = request.GET['place_id']
	
	likes = 0
	if place_id:
		place = Place.objects.get(id=int(place_id))
		if place:
			likes = place.likes +1
			place.likes = likes
			request.session[str(place.id)+'_has_liked'] = True
			print request.session[str(place.id)+'_has_liked']
			place.save()
	
	return HttpResponse(likes)	


def page(request, page_url):
	context = RequestContext(request)
	nav = Page.objects.all()
	context_dict = {}
	context_dict['nav'] = nav
	
	try:
		page = Page.objects.get(local_url=page_url)
		context_dict['page'] = page
	
	except Page.DoesNotExist:
		pass
	
	return render_to_response('maps/page.html', context_dict, context)


def search(request):
		
	return basic_search(request, extra_context={
		'nav': Page.objects.all(),
		'map': Map.objects.get(title="Tower Hamlets"),
		'layers': Layer.objects.all(),
		})