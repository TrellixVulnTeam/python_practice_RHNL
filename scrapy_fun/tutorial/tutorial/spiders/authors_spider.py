import scrapy


class AuthorsSpider(scrapy.Spider):  # define a class
    name = "authors"  # define the variable,identifies the Spider.Must be unique.
# allowed_domains = ["toscrape.com"]
    start_urls = ["http://quotes.toscrape.com"]

    # call back method
    def parse(self, response):
        urls = response.css('div.quote > span > a::attr(href)').extract()
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_details)
        # follow pagination link
            # this line just gets the relative url
        next_page_url = response.css('li.next > a::attr(href)').extract_first()
        if next_page_url:  # spider will stop once there're no more pages
            next_page_url = response.urljoin(next_page_url)
            # the spider needs to generate new request
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_details(self, response):
        yield {
            'name': response.css('h3.author-title::text').extract_first(),
            'birth_date': response.css('span.author-born-date::text').extract_first()
        }
