from haystack import indexes
from maps.models import Place, Map, Page, Layer, Activity

class PlaceIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True)
	title = indexes.CharField(model_attr='title')
	description = indexes.CharField(model_attr='description')
	
	def get_model(self):
		return Place
	
	def index_queryset(self, using=None):
		return self.get_model().objects.all()
