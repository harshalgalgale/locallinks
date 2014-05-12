from haystack import indexes
from maps.models import Place, Person

class AssetIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True)
	title = indexes.CharField(model_attr='title')
	type = indexes.CharField(model_attr='type')
	
	def get_model(self):
		return Place

class PersonIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True)
	firstname = indexes.CharField(model_attr='first_name')
	lastname = indexes.CharField(model_attr='last_name')
	bio = indexes.CharField(model_attr='bio')
	
	def get_model(self):
		return Person