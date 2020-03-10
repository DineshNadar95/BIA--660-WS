from bs4 import BeautifulSoup
import re
import time
import requests


def run(url):
    ct=0
    pageNum=2 # number of pages to collect

    fw=open('reviews.txt','w') # output file
	
    for p in range(1,pageNum+1): # for each page 

        #print ('page',p)
        html=None

        if p==1: pageLink=url # url for page 1
        else: pageLink=url+'?page='+str(p)+'&sort=' # make the page url
		
        for i in range(5): # try 5 times
            try:
                #use the browser to access the url
                response=requests.get(pageLink,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
                html=response.content # get the html
                break # we got the file, break the loop
            except Exception as e:# browser.open() threw an exception, the attempt to get the response failed
                print ('failed attempt',i)
                time.sleep(2) # wait 2 secs
				
		
        if not html:continue # couldnt get the page, ignore
        
        soup = BeautifulSoup(html.decode('ascii', 'ignore'),'lxml') # parse the html 
        #source=soup.findAll('meta',{'property':'og:site_names'},{'content'})
        source=soup.find("meta", property="og:site_name") #gets the source
        source=source["content"]
        reviews=soup.findAll('div', {'class':re.compile('review_table_row')}) # get all the review divs

        for review in reviews:
            ct=ct+1
            critic,text,date,rating='NA','NA','NA','NA' # initialize critic and text 
            criticChunk=review.find('a',{'href':re.compile('/critic/')})
            if criticChunk: critic=criticChunk.text#.encode('ascii','ignore')
            else: critic='NA'

            textChunk=review.find('div',{'class':'the_review'})
            if textChunk: text=textChunk.text.strip() #.encode('ascii','ignore')	
            else: text='NA'

            dateChunk=review.find('div',{'class':'review-date subtle small'})
            if dateChunk: date=dateChunk.text.strip()
            else: date='NA'
            
            sourceChunk=review.find('em',{'class':'subtle'})
            if sourceChunk: source=sourceChunk.text#.encode('ascii','ignore')	

            if review.find('div',{'class' : 'review_icon icon small rotten'}):
                rating = 'rotten'
            elif review.find('div',{'class' : 'review_icon icon small fresh'}):
                rating = 'fresh' 
            else:
                rating = 'NA'
            if(not source): source="NA"
            source=str(source)

            fw.write(critic.ljust(20)+'\t'+rating.ljust(6)+'\t'+source.ljust(35)+'\t'+text.ljust(240)+'\t'+date+'\n') # write to file 
		
        
   # print(ct) - count of the reviewers 
    fw.close()

if __name__=='__main__':
    url='https://www.rottentomatoes.com/m/space_jam/reviews/'
    run(url)

