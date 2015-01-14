from django.shortcuts import render
from clsearcher.models import EntryMaster, EntryDetail, EntrySearch
from django.views.generic import TemplateView, View, ListView
from django.http import HttpResponse
import simplejson
from django.views.decorators.csrf import csrf_exempt
from clTroller import Troller
from django.core import serializers
from django.template import RequestContext, loader, RequestContext
from django.shortcuts import render, render_to_response

class Main(ListView):
	template_name = 'main.html'
	model = EntryMaster
	#def mainView(request):
	    #t = loader.get_template('main.html')
	    #groups = EntryMaster.objects.all()
	    #c = Context({'group':groups}) 
	    
	    #old fashioned fallback - being depricated in 1.6
	    #return render_to_response(template_name, {'groups':groups}, context_instance = RequestContext(request))

	    #not working!!
	    #return HttpResponse(t.render(c))


class UpdateView(TemplateView):
	template_name = "clsearch.html"
	
	def get(self, request):
	    group = request.GET.get('group')
	    search = request.Get.get('search')
	    t = Troller(group, search)
	    t.get()
	    t.parseMainSearch()
	    t.getEntryDetails()
	    t.sendEntries()

	    try:
		g = EntryGroup.objects.get(EntryGroup = group)
		msg = serlalizers.serlialize('json', msg)
	    except:
		msg = {'error':'something janged up'}
		simplejson.dumps(msg)
	    return HttpResponse(msg)

class NewEntry(TemplateView):
	def post(self, request):
	    try:
                incomingEntry = simplejson.loads(request.body)
	    except:
		msg = {'error':'could not load request'}
		msg = simplejson.dumps(msg)
		print 'POST: ',request.POST, 'Body: ',request.body, 'Request: ', request.REQUEST
		return HttpResponse(msg)

	    try:
	        group = EntryMaster.objects.get(EntryGroup = incomingEntry['entryGroup'])
		print incomingEntry['entryGroup']
	    except:
		group = EntryMaster.objects.create(EntryGroup = incomingEntry['entryGroup'])
		print 'created new group! ', group.EntryGroup

	    try:
		search = EntrySearch.objects.get(EntryGroup = group, EntrySearch = incomingEntry['entrySearch'])
 	    except:
		search = EntrySearch.objects.create(EntryGroup = group, EntrySearch = incomingEntry['entrySearch'])
		print 'created new search! ', search.EntrySearch
	
	    try:
		entry = EntryDetail.objects.get(EntryCLID = incomingEntry['clid'])
		print 'result : success, but object already exitsts', entry.EntryTitle
	    except:
		entry = EntryDetail.objects.create(EntryType = search, EntryTitle = incomingEntry['entryTitle'], EntryDescription = incomingEntry['entryDescription'], EntryPrice=incomingEntry['entryPrice'], EntryURL = incomingEntry['entryURL'], EntryCLID=int(incomingEntry['clid']))
		entry.save()
		msg = {'result':'successfully saved entry!','entry':entry.EntryTitle}
		
	    msg = simplejson.dumps(msg)

	    return HttpResponse(msg)



