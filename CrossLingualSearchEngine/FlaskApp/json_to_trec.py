import json
# if you are using python 3, you should 
#import urllib.request 
import urllib2


# change the url according to your own corename and query
#inurl = 'http://localhost:8983/solr/corename/select?q=%3A&fl=id%2Cscore&wt=json&indent=true&rows=1000'
def functionName(query):
	inurl = 'http://54.165.143.30:8983/solr/IRF19P1/select?facet.query=' + query + '&facet=on&q=*%3A*&rows=50&wt=json'
	print inurl


# change query id and IRModel name accordingly
	qid = ''
	IRModel='default'
	#outf = open(outfn, 'a+')
	data = urllib2.urlopen(inurl)
# if you're using python 3, you should use
# data = urllib.request.urlopen(inurl)

	docs = json.load(data)['response']['docs']
# the ranking should start from 1 and increase
	result = ""
	for doc in docs:
		result += doc['full_text'][0]

	return result
	
print(functionName('modi').encode("utf-8"))