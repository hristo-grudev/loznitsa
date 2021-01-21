BOT_NAME = 'loznitsa'

SPIDER_MODULES = ['loznitsa.spiders']
NEWSPIDER_MODULE = 'loznitsa.spiders'
FEED_EXPORT_ENCODING = 'utf-8'
LOG_LEVEL = 'ERROR'
DOWNLOAD_DELAY = 0

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
	'loznitsa.pipelines.LoznitsaPipeline': 100,

}