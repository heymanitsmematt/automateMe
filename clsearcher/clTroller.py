import requests
import re
import simplejson
import sys

searchKeys = ['Galaxy Note 3']

class Troller:
	def __init__(self, group, key):
	    self.url = 'http://washingtondc.craigslist.org/search/sss?sort=rel&query='+key.replace(' ','+')
	    self.mainURL = 'http://washingtondc.craigslist.org/'
	    self.searchKey = key
	    self.group = group

	def get(self):
	    self.request = requests.get(self.url, timeout=5.0)

	def parseMainSearch(self):
	    thisLink = ''
	    self.entries = []
	    self.rawContent = self.request.text[self.request.text.find('<div class="content">'):self.request.text.find('<div class="toc_legend bottom">')]
	    for link in self.rawContent.split('<p'):
		try:
		    thisLink = link[[m.start() for m in re.finditer(r"<a href=",link)][1]:]
		    proceed='t'
		except:
		    print 'fail 1 on ', link[25:50]
		    proceed='f'
		if proceed=='t' and thisLink != '':
		    try:    
			thisLink = thisLink[10:]
			self.thisLink = thisLink
		        thisLinkURL = thisLink[:thisLink.find('"')]
		        thisLinkCLID = thisLinkURL.split('/')[2][:-5]
			thisLinkTitle = thisLink[thisLink.find('>')+1:thisLink.find('</a>')]
		        thisLinkPrice = thisLink[thisLink.find('price')+6:]
		        thisLinkPrice = thisLinkPrice[thisLinkPrice.find(';')+1:thisLinkPrice.find('<')]
		        self.entries.append((thisLinkURL, thisLinkTitle, thisLinkPrice, thisLinkCLID))
		    except:
		        print thisLink[:25]
		
	    return self.entries

	def getEntryDetails(self):
	    self.rawDetails = []
	    for pair in self.entries:
		thisURL = self.mainURL + pair[0]
		thisRequest = requests.get(thisURL)
		thisRequestDetails = thisRequest.text[thisRequest.text.find('<section id="postingbody">'):thisRequest.text.find('do NOT contact me with unsolicited services')]
		self.rawDetails.append((pair[0],pair[1], pair[2], thisRequestDetails, pair[3]))
	
	def sendEntries(self):
	    for item in self.rawDetails:
		thisRequestDict = {}
		thisRequestDict['clid'] = item[4] #pair[3]
		thisRequestDict['entryGroup'] = self.group
		thisRequestDict['entrySearch'] = self.searchKey
		thisRequestDict['entryTitle'] = item[1] 
		thisRequestDict['entryDescription'] = item[3]
		thisRequestDict['entryPrice'] = item[2]
		thisRequestDict['entryURL'] = item[0]
		self.lastRequestDict = thisRequestDict
		json = simplejson.dumps(thisRequestDict)
		
		try:
		    self.thisRequest = requests.post('http://10.89.30.244:8080/clsearcher/NewEntry/',data=json, timeout=5.0)
		    print self.thisRequest
	        except:
		    print 'error sending to new entry view'

#t = Troller(searchKeys[0])
#t.get()
#t.parseMainSearch()
#t.getEntryDetails()


