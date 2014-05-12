from django.contrib import admin
from maps.models import Map, Layer, Type, Place, City, Quote, Person, Role, Page

def make_published(modeladmin, request, queryset):
	queryset.update(published=True)
make_published.short_description = "Put selected assets on the map"

def un_publish(modeladmin, request, queryset):
	queryset.update(published=False)
un_publish.short_description = "Remove selected assets from the map"


class QuoteInline(admin.TabularInline):
	model = Quote

class RoleInline(admin.TabularInline):
	model = Role

class PlaceAdmin(admin.ModelAdmin):
    fieldsets = [
        ('About the asset',		{'fields': ['title', 'map', 'type', 'layer', 'published', 'likes', 'thumbnail']}),
        ('Address', 			{'fields': ['address_1', 'address_2', 'address_3', 'city', 'postcode']}),
        ('Contact details',		{'fields': ['phone', 'email', 'url']}),
    ]
    list_display = ('title', 'lat', 'lon', 'type', 'published')
    inlines = [
    	QuoteInline,
    	RoleInline
    ]
    actions = [make_published, un_publish]

class TypeAdmin(admin.ModelAdmin):
	list_display = ('title', 'layer')

admin.site.register(Map)
admin.site.register(Layer)
admin.site.register(Type, TypeAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Person)
admin.site.register(City)
admin.site.register(Page)