import json
import re
from copy import deepcopy
from urllib.parse import urlencode

import scrapy
from scrapy.http import HtmlResponse

from instagrams.items import InstagramsItem


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    inst_login = 'Onliskill_udm'
    inst_passw = '#PWD_INSTAGRAM_BROWSER:10:1643131213:AZZQAGTPs6xfu+lt7ppOoFuIqKbWrZ4VaEX53g+SZCn8PJlFrepy7g4RoBJ9hG8g+yNb2R3TWGMrJek2u4SWHgpXYJPp7CijVJirea6j+tAGshfXR9HonVrpXtM9HF0oH+v2RlGNdeDqkBSgLuKb'
    user_for_pase = ['spxtech333', "asep_ramdan455"]
    url_api = 'https://i.instagram.com/api/v1/friendships/'
    posts_hash = '8c2a529969ee035a5063f2fc8602a0fd'

    def parse(self, response: HtmlResponse):
        csrf_token = self.fetch_csrf_token(response.text)

        yield scrapy.FormRequest(self.inst_login_link,
                                 method='POST',
                                 callback=self.login,
                                 formdata={'username': self.inst_login,
                                           'enc_password': self.inst_passw},
                                 headers={'X-CSRFToken': csrf_token})

    def login(self, response: HtmlResponse):
        j_data = response.json()
        if j_data['authenticated']:
            for item in self.user_for_pase:
                print(item)
                yield response.follow(f'/{item}',
                                      callback=self.user_parse,
                                      cb_kwargs={'username': item,
                                                 "follows": [{"followers": "max_id", "following": "next_max_id"}]})

    def user_parse(self, response: HtmlResponse, username, follows):
        user_id = self.fetch_user_id(response.text, username)
        for follow_items in follows:
            for follow_item, key in follow_items.items():
                variables = {'id': user_id,
                             'count': 12,
                             f"{key}": 12,
                             "search_surface": "follow_list_page"}
                url = f'{self.url_api}{variables["id"]}/{follow_item}/?{urlencode(variables)}'

                yield response.follow(url,
                                      callback=self.user_posts_parse,
                                      cb_kwargs={'username': username,
                                                 'user_id': user_id,
                                                 'follow_item': follow_item,
                                                 'key': key,
                                                 'variables': deepcopy(variables)})

    def user_posts_parse(self, response: HtmlResponse, username, user_id, follow_item, key, variables):
        j_data = response.json()
        if j_data.get('big_list'):
            variables[key] += variables['count']

            url = f'{self.url_api}{variables["id"]}/{follow_item}/?{urlencode(variables)}'

            yield response.follow(url,
                                  callback=self.user_posts_parse,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id,
                                             'follow_item': follow_item,
                                             'key': key,
                                             'variables': deepcopy(variables)})

        posts = j_data.get('users')

        for post in posts:
            item = InstagramsItem(
                _id=int(post.get("pk")),
                username=post.get("username"),
                photo=post.get('profile_pic_url'),
                follow=follow_item
            )
            yield item

    def fetch_csrf_token(self, text):
        ''' Get csrf-token for auth '''
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        try:
            matched = re.search(
                '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
            ).group()
            return json.loads(matched).get('id')
        except:
            return re.findall('\"id\":\"\\d+\"', text)[-1].split('"')[-2]
