from django.contrib import admin
from django import forms
from maps.models import Map, Layer, Place, City, Quote, Page, Activity, Photo, ActivityQuote
from image_cropping import ImageCroppingMixin

def make_published(modeladmin, request, queryset):
	queryset.update(published=True)
make_published.short_description = "Put selected assets on the map"

def un_publish(modeladmin, request, queryset):
	queryset.update(published=False)
un_publish.short_description = "Remove selected assets from the map"


class QuoteInline(admin.TabularInline):
	model = Quote

class ActivityInline(admin.TabularInline):
	model = Activity


class ActivityQuoteInline(admin.TabularInline):
	model = ActivityQuote
	
	def formfield_for_dbfield(self, field, **kwargs):
		if field.name == 'activity':
			parent_place = self.get_object(kwargs['request'], Place)
			activities = Activity.objects.filter(place=parent_place)
			return forms.ModelChoiceField(queryset=activities)
		return super(ActivityQuoteInline, self).formfield_for_dbfield(field, **kwargs)	
	
	def get_object(self, request, model):
		"""A nasty hack to get the parent model instance"""
		object_id = request.META['PATH_INFO'].strip('/').split('/')[-1]
		try:
			object_id = int(object_id)
		except ValueError:
			return None
		return model.objects.get(pk=object_id)
	
	
class PhotoInline(admin.TabularInline):
	model = Photo

class PlaceAdmin(ImageCroppingMixin, admin.ModelAdmin):
    fieldsets = [
        ('About the asset',		{'fields': ['title', 'local_url', 'map', 'layer', 'published', 'likes', 'thumbnail', 'cropping', 'description', 'tags']}),
        ('Address', 			{'fields': ['address_1', 'address_2', 'address_3', 'city', 'postcode']}),
        ('Contact details',		{'fields': ['phone', 'email', 'url', 'directory_url']}),
    ]
    list_display = ('title', 'lat', 'lon', 'published')
    inlines = [
    	QuoteInline,
    	ActivityInline,
    	ActivityQuoteInline,
    	PhotoInline,
    ]
    prepopulated_fields = { 'local_url': ['title']}
    actions = [make_published, un_publish]

class PageAdmin(admin.ModelAdmin):
	prepopulated_fields = { 'local_url': ['title']}

admin.site.register(Map)
admin.site.register(Layer)
admin.site.register(Place, PlaceAdmin)
admin.site.register(City)
admin.site.register(Page, PageAdmin)
admin.site.register(ActivityQuote)