# -*- coding: utf-8 -*-
from lxml import etree
from multiprocessing.dummy import Pool as ThreadPool
import requests
import time
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def finsh(contentdict):
	f.writelines(str(contentdict['isFinish?']))

def towrite(contentdict):
	# f.writelines(str(contentdict['song_Lable'])+" ,")
	f.writelines(str(contentdict['song_Author'])+" ,")
	f.writelines(str(contentdict['song_name'])+" "+'\n')

def lyrics(url):
	html = requests.get('http://lyrics.wikia.com/wiki/'+url)
	selector = etree.HTML(html.text)
	item = {}
	lyrics=""
	print "running"
	content_field=selector.xpath('//*[@id="mw-content-text"]/div[@class="lyricbox"]/text()')
	for each in content_field:
		lyrics=lyrics+each+' '
	return lyrics.replace('\n','')

def musiclist(url):
	html = requests.get('http://lyrics.wikia.com/wiki/'+url)
	selector = etree.HTML(html.text)
	item = {}
	musicList=[]
	content_field=selector.xpath('//*[@id="mw-content-text"]')
	for each in content_field:
		cont=each.xpath('ol')
		if cont==[]:
			return ""
		for j in range(1,len(cont)+1):

			cont1=each.xpath('ol['+str(j)+']/li')
			for i in range(1,len(cont1)+1):
				lyricsList=[]
				content=each.xpath('ol['+str(j)+']/li['+str(i)+']/b/a/text()')[0]
				content2=content.replace(' ','_').replace('&','%26')
				content3=url+":"+content2
				lyricsList.append(content3)
				results_musicPage=pool.map(lyrics,lyricsList)
				# 歌詞空的則不打印
				if results_musicPage[0]=="":
					continue
				# print "musicList: "+str(j*len(cont)+i)
				content_name_lyrics=content2+" ,"+results_musicPage[0].replace(',',' ').replace('.',' ')
				try:
					musicList.append(content_name_lyrics)
				except IndexError:
					continue
		return musicList

def author(url):
	html = requests.get('http://lyrics.wikia.com/wiki/Category:'+url)
	selector = etree.HTML(html.text)
	item = {}
	cont=selector.xpath('//*[@id="mw-pages"]/div/table/tr/td')
	for i in range(1,len(cont)+1):
		content_field2 = selector.xpath('//*[@id="mw-pages"]/div/table/tr/td['+str(i)+']')
		cont1=selector.xpath('//*[@id="mw-pages"]/div/table/tr/td['+str(i)+']/ul')
		if content_field2==[]:
			content_field2=selector.xpath('//*[@id="mw-pages"]/div')
			if content_field2==[]:
				continue
		for j in range(1,len(cont1)+1):
			cont2=selector.xpath('//*[@id="mw-pages"]/div/table/tr/td['+str(i)+']/ul['+str(j)+']/li')
			for k in range(1,len(cont2)+1):
				authorList=[]
				content=content_field2[0].xpath('ul['+str(j)+']/li['+str(k)+']/a/text()')[0]
				content2=content.replace(' ','_').replace('&','%26')
				item['song_Lable']=url.replace('_',' ').replace('%26','&').replace('Label/','')
				item['song_Author']=content2.replace('_',' ').replace('%26','&')
				authorList.append(content2)
				try:
					results_authorPage=pool.map(musiclist,authorList)
				except Exception:
					continue
				for eh in results_authorPage:
					for e in eh:
						if e=="":
							print "nnnnnnnnnnnnn"
						item['song_name']=e.replace('_',' ').replace('%26','&')
						towrite(item)

# 爬蟲函數
def lable(url):
	html = requests.get(url)
	selector = etree.HTML(html.text)
	item = {}
	# 列數量
	cont=selector.xpath('//*[@id="mw-subcategories"]/div/table/tr/td')
	for i in range(1,len(cont)+1):
		content_field = selector.xpath('//*[@id="mw-subcategories"]/div/table/tr/td['+str(i)+']')
		cont1=selector.xpath('//*[@id="mw-subcategories"]/div/table/tr/td['+str(i)+']/ul')
		for k in range(1,len(cont1)+1):
			cont2=selector.xpath('//*[@id="mw-subcategories"]/div/table/tr/td['+str(i)+']/ul['+str(k)+']/li')
			for j in range(1,len(cont2)+1):
				musicPage = []
				content = content_field[0].xpath('ul['+str(k)+']/li['+str(j)+']/div/div/a/text()')[0]
				content2=content.replace(' ','_').replace('&','%26')
				musicPage.append(content2)
				results_labelPage=pool.map(author,musicPage)


if __name__ == '__main__':
	pages=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
	pool = ThreadPool(4)
	f = open('song_labels_T.txt', 'a')
	page = ['http://lyrics.wikia.com/wiki/Category:Label?from=T']
	results = pool.map(lable, page)
	pool.close()
	pool.join()
	f.close()

	f=open('Job_Finished.txt','a')
	item={}
	item['isFinish?']="Job Finished!!!"
	finsh(item)
	f.close


