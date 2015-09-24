#! /usr/bin/env python

# Make a new script to build a custom comics page every day

import urllib2
import re
import datetime
import inspect

class getComics(object):
    def __init__(self):
        self.today = datetime.date.today()
        self.hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
        self.getFuncs=[]
        for p in inspect.getmembers(self, predicate=inspect.ismethod):
            if p[0].startswith('get'):
                self.getFuncs.append(p[1])

    def run(self):
        content = ''
        for func in self.getFuncs:
            result = func()
            for res in result:
                content += '<br>'+res +'\n'
            content += '<hr>'
        return content

    def getDilbert(self):
        dil_page = urllib2.urlopen('http://www.dilbert.com/').read()
        spot = dil_page.find("http://assets.amuniversal")
        dil_page = dil_page[spot-20:spot+100].replace("\n","")
        dil_page = re.sub('.*http', 'http', dil_page)
        dil_page = re.sub('".*','',dil_page)
        result = '<IMG SRC="'+dil_page+'">'
        return [result]

    def getDoons(self):
        result = '<IMG SRC="http://images.ucomics.com/comics/db/20'
        if self.today.weekday() == 6:
            filetype='.jpg'
        else:
            filetype = '.gif'
        result = result + self.today.strftime('%y/db%y%m%d')+filetype+'">'
        return [result]

    #def getNonSeq(self):
        #result = '<IMG SRC="http://images.ucomics.com/comics/nq/20'
        #result = result + self.today.strftime('%y/nq%y%m%d') +'.gif">'
        #return [result]
        #pass

    def getSMBC(self):
        page = urllib2.urlopen('http://www.smbc-comics.com/').read()
        spot = page.find('comicbody')
        main_comic = page[spot:spot+200].replace('\n','')
        main_comic = re.sub( '.*src="','',main_comic)
        main_comic = re.sub('png.*', 'png', main_comic)
        result1 = "<img src='http://www.smbc-comics.com/"+main_comic+"'>"

        spot = page.find('extracomic')
        after = page[spot:spot+300].replace('\n','')
        after = re.sub(".*src=.",'',after)
        after = re.sub('png.*', 'png', after)
        result2 = "<img src='"+after+"'>"
        return [result1, result2]

    def getJandMo(self):
        req = urllib2.Request('http://www.jesusandmo.net', headers=self.hdr)
        page = urllib2.urlopen(req).read()
        spot = page.find('/strips')
        comic = page[spot-40:spot+80].replace('\n','')
        comic = re.sub('.*<img','<img',comic)
        comic = re.sub('>.*','>',comic)
        return [comic]

    def getPhD(self):
        result = ''
        for i in range(5)[::-1]:
            try:
                blah = urllib2.urlopen("http://www.phdcomics.com/comics/archive/phd"+ self.today.replace(day=self.today.day-i).strftime('%m%d%y')+'s.gif').code
                if blah/100 < 4:
                    result = '<img id=comic name=comic src=http://www.phdcomics.com/comics/archive/phd'+self.today.replace(day=self.today.day-i).strftime('%m%d%y')+'s.gif border=0 align=top>'
            except:
                pass
        return [result]

    def getXkcd(self):
        page = urllib2.urlopen('http://xkcd.com/').read()
        spot = page.find('imgs.xkcd.com/comics')
        comic = page[spot-18:spot+400].replace('\n','')
        comic = re.sub('.*imgs', 'imgs',comic)
        comic = re.sub('png.*','png',comic)
        comic = '<img src="http://'+comic +'">'
        alt = page[spot-18:spot+400].replace('\n','')
        alt = re.sub('.*title="','', alt)
        alt = re.sub('".*', '', alt)
        return [comic,alt]

    def getFT(self):
        req = urllib2.Request('http://www.gocomics.com/foxtrot', headers=self.hdr)
        page = urllib2.urlopen(req).read()
        spot = page.find('class="strip"')
        comic = page[spot-100:spot+100].replace('\n','')
        comic = re.sub('>.*','>',re.sub('.*<img','<img',comic))
        return [comic]

    def obsolete_getAbG(self):
        page = urllib2.urlopen('http://abstrusegoose.com/').read()
        spot = page.find('png')
        comic = page[spot-100:spot+150].replace('\n','')
        comic = re.sub('>.*','>',re.sub('.*<img','<img',comic))
        return [comic]

    def getTWW(self):
        page = urllib2.urlopen('http://www.dailykos.com/blog/Comics').read()
        spot = page.find('TMW')
        comic = page[spot-100:spot+75].replace('\n','')
        comic = re.sub('<span class.*','',comic)

        comic =re.sub('.*<a rel="lightbox" href=','<img src=',comic)
        return [comic]

    def getFowl(self):
        req = urllib2.Request('http://www.fowllanguagecomics.com/', headers=self.hdr)
        page = urllib2.urlopen(req).read()
        spot = page.find('id="comic"')
        comic = page[spot:spot+500]
        spot2= comic.find('<img src="')
        comic = comic[spot2:]
        spot2 = comic.find("</div>")
        result = [comic[:spot2]]

        if "Bonus Panel" in page:
            spot = page.find('Bonus Panel"><img src')
            comic = page[spot:spot+400]
            spot2 = comic.find('<img src')
            comic = comic[spot2:]
            spot2 = comic.find('/>')
            comic = comic[:spot2+2]
            result.append(comic)

        return result



if __name__ == "__main__":

    outfile = open('index.html','w')

    web_page = '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"> \n <html> \n <head>\n   <meta content="text/html; charset=ISO-8859-1"\n  http-equiv="content-type">\n   <title>Custom Comics Page</title>\n </head>\n <body>\n'

    gc = getComics()
    web_page += gc.run()
    web_page += '<!-- Start of StatCounter Code --> \n <script type="text/javascript" language="javascript">\n var sc_project=1310929; \n var sc_invisible=1; \n var sc_partition=9; \n var sc_security="f5c1bdfd"; \n </script>\n \n <script type="text/javascript" language="javascript" src="http://www.statcounter.com/counter/counter.js"></script><noscript><a href="http://www.statcounter.com/" target="_blank"><img  src="http://c10.statcounter.com/counter.php?sc_project=1310929&java=0&security=f5c1bdfd&invisible=1" alt="free hit counter javascript" border="0"></a> </noscript>\n <!-- End of StatCounter Code -->\n </body>\n </html>'

    print >>outfile, web_page
