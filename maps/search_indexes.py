from haystack import indexes
from maps.models import Place

class AssetIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True)
	title = indexes.CharField(model_attr='title')
	description = indexes.CharField(model_attr='description')
	
	def get_model(self):
		return Place