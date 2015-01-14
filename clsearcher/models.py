from django.db import models


class EntryMaster(models.Model):
	EntryGroup = models.CharField(max_length=50, null=False)
	
	def __unicode__(self):
	    return self.EntryGroup

class EntrySearch(models.Model):
	EntryGroup = models.ForeignKey(EntryMaster)
	EntrySearch = models.CharField(max_length=100)

	def __unicode__(self):
	    return self.EntrySearch

class EntryDetail(models.Model):
	EntryType = models.ForeignKey(EntrySearch)
	EntryTitle = models.CharField(max_length=100)
	EntryDescription = models.CharField(max_length=500000, null=True)
	EntryPrice = models.DecimalField(max_digits=10, decimal_places=2, null=True)
	EntryDateCreated = models.DateField(auto_now_add=True)
	#EntryPostedDate = models.DateField(null=False)
	EntryURL = models.CharField(max_length=200, null=False)
	EntryCLID = models.BigIntegerField(null=False)
	EntryActiveFlag = models.BooleanField(default=True)

	def __unicode__(self):
	    return self.EntryTitle

	def bestDeal(self):
	    return self.objects.filter(EntryType__exact=entryType).aggregate(Min('EntryPrice'))
