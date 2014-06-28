from django.contrib import admin
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
	fk_name = "place"
	
	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		place = request.META['PATH_INFO'].strip('/').split('/')[-1]
		if db_field.name == 'activity':
			kwargs["queryset"] = Activity.objects.filter(place=place)
		return super(ActivityQuoteInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

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