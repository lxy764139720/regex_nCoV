import re
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup

from news_word_cloud.items import Article


class ArticleSpider(scrapy.Spider):
    name = 'article'
    allowed_domains = ['lianghui.people.com.cn']
    start_urls = ['http://lianghui.people.com.cn/2021npc/GB/437015/index1.html',
                  'http://lianghui.people.com.cn/2021npc/GB/437015/index2.html',
                  'http://lianghui.people.com.cn/2021npc/GB/437015/index3.html',
                  'http://lianghui.people.com.cn/2021npc/GB/437015/index4.html',
                  'http://lianghui.people.com.cn/2021npc/GB/437033/index1.html',
                  'http://lianghui.people.com.cn/2021npc/GB/437033/index2.html',
                  'http://lianghui.people.com.cn/2021npc/GB/437033/index3.html',
                  'http://lianghui.people.com.cn/2021npc/GB/437033/index4.html',
                  'http://lianghui.people.com.cn/2021npc/GB/437033/index5.html']
    rules = [Rule(LinkExtractor(allow=r'.*'),
                  callback='parse',
                  follow=True)]

    def parse(self, response, **kwargs):
        article = Article()
        bs = BeautifulSoup(response.body, "lxml")
        if bs.find('h1', {'id': 'p_title'}):
            # 文章页面
            article['url'] = response.url
            article['title'] = bs.find('h1', {'id': 'p_title'}).get_text().replace('\xa0', '')
            text = ''
            for content in bs.find('div', {'id': 'p_content'}).children:
                if content.name == 'p':
                    # print(content.get_text())
                    text += content.get_text()
            article['text'] = text.replace('\n', '').replace('\r', '').replace('\t', '') \
                .replace('\xa0', '').replace(u'\u3000', u'').replace(' ', '').replace(',', '，')
            # 20210306
            article['date'] = '2021' + re.findall(r'/2021npc/n1/2021/([0-9]{4})/[^/]+?.html', response.url)[0]
            yield article
        else:
            # 索引页面
            # print(response.body.decode('GBK'))
            for url in re.findall(r'/2021npc/n1/2021/[0-9]{4}/[^/]+?.html', response.body.decode('GBK')):
                # print(url)
                yield scrapy.Request('http://lianghui.people.com.cn' + url, callback=self.parse)
