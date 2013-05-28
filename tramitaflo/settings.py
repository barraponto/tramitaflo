# Scrapy settings for tramitaflo project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'tramitaflo'

SPIDER_MODULES = ['tramitaflo.spiders']
NEWSPIDER_MODULE = 'tramitaflo.spiders'

CONCURRENT_REQUESTS = 8

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tramitaflo (+http://www.yourdomain.com)'
