######################################################################################
#
#	EngSub.org - v0.10
#
######################################################################################

TITLE = "EngSub"
PREFIX = "/video/engsub"
ART = "art-default.jpg"
ICON = "icon-default.png"
ICON_LIST = "icon-list.png"
ICON_COVER = "icon-cover.png"
ICON_NEXT = "icon-next.png"
BASE_URL = "http://engsub.org"

######################################################################################
# Set global variables

def Start():

	ObjectContainer.title1 = TITLE
	ObjectContainer.art = R(ART)
	DirectoryObject.thumb = R(ICON_LIST)
	DirectoryObject.art = R(ART)
	VideoClipObject.thumb = R(ICON_LIST)
	VideoClipObject.art = R(ART)
	
	HTTP.CacheTime = CACHE_1HOUR
	HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'
	HTTP.Headers['Referer'] = 'http://engsub.org/'
	
######################################################################################
# Menu hierarchy

@handler(PREFIX, TITLE, art=ART, thumb=ICON)
def MainMenu():

	oc = ObjectContainer()
	page = HTML.ElementFromURL(BASE_URL)
	for each in page.xpath("//ul[@class='sub-menu']/li[contains(@class,'category')]"):
		title = each.xpath("./a/text()")[0]
		category = each.xpath("./a/@href")[0]
		oc.add(DirectoryObject(
			key = Callback(ShowCategory, title = title, category = category, page_count = 1),
			title = title,
			thumb = R(ICON_LIST)
			)
		)

	return oc

######################################################################################
# Creates page url from category and creates objects from that page

@route(PREFIX + "/showcategory")	
def ShowCategory(title, category, page_count):

	oc = ObjectContainer(title1 = title)
	thistitle = title
	page = HTML.ElementFromURL(str(category) + '/page/' + str(page_count))
	for each in page.xpath("//div[@class='inner']"):
		url = each.xpath("./a/@href")[0]
		title = each.xpath("./a/@title")[0]
		thumb = each.xpath("./a/img/@src")[0]
		if "Season" not in title:
			oc.add(DirectoryObject(
				key = Callback(EpisodeDetail, title = title, url = url),
				title = title,
				thumb = Resource.ContentsOfURLWithFallback(url = thumb, fallback='icon-cover.png')
				)
			)

	oc.add(NextPageObject(
		key = Callback(ShowCategory, title = thistitle, category = category, page_count = int(page_count) + 1),
		title = "More...",
		thumb = R(ICON_NEXT)
			)
		)
	
	return oc

######################################################################################
# Gets metadata and google docs link from episode page. Checks for trailer availablity.

@route(PREFIX + "/episodedetail")
def EpisodeDetail(title, url):
	
	oc = ObjectContainer(title1 = title)
	page = HTML.ElementFromURL(url)
	title = page.xpath("//meta[@property='og:title']/@content")[0]
	description = page.xpath("//meta[@property='og:description']/@content")[0]
	thumb = page.xpath("//div[@class='poster']/img/@src")[0]
	
	oc.add(VideoClipObject(
		title = title,
		summary = description,
		thumb = thumb,
		url = url
		)
	)	
	
	return oc	
