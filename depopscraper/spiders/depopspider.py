import scrapy
import json
import base64
import datetime

timestamp = datetime.datetime.now().timestamp()

class DepopspiderSpider(scrapy.Spider):
    global timestamp
    name = "depopspider"
    allowed_domains = ["depop.com"]
    start_urls = ["https://webapi.depop.com/api/v3/search/products/?what=&cursor=M3w0OHwxNzY4Mzk3NzQ4&items_per_page=24&country=de&currency=EUR&groups=tops,bottoms,coats-jackets,footwear,jumpsuit-and-playsuit,dresses,suits&is_kids=false&gender=male&force_fee_calculation=false&from=in_country_search"]
    current_page = 1
    current_offset = 24
    current_timestamp = 1768402135

    def generate_next_cursor(self, page_num, offset, timestamp):
        raw_string = f"{page_num}|{offset}|{timestamp}"
        b64_bytes = base64.b64encode(raw_string.encode("ascii"))
        return b64_bytes.decode("ascii")


    def parse(self, response):
        json_data = json.loads(response.body)
        items = json_data["products"]
        if not items:
            return
        for item in items:
            yield {
                "Name": item["slug"],
                "Price": "€" + item["pricing"]["original_price"]["total_price"],
                "Size": item["sizes"][0],
                "Brand name": item["brand_name"],
                "Link": "https://www.depop.com/products/" + item["slug"],
            }
        self.current_page += 1
        self.current_offset += 24
        next_cursor = self.generate_next_cursor(self.current_page, self.current_offset, self.current_timestamp)

        yield scrapy.Request(f"https://webapi.depop.com/api/v3/search/products/?what=&cursor={next_cursor}&items_per_page=24&country=de&currency=EUR&groups=tops,bottoms,coats-jackets,footwear,jumpsuit-and-playsuit,dresses,suits&is_kids=false&gender=male&force_fee_calculation=false&from=in_country_search", meta={"cursor": next_cursor}, callback=self.parse)
