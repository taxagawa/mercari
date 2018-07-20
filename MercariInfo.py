# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import, unicode_literals
from selenium import webdriver
from SendToSlack import send_to_slack

#ヘッドレスブラウザ使用
options = webdriver.ChromeOptions()
options.add_argument('--headless')

#Googleにアクセスして、タイトルをとってこれるかテスト
browser = webdriver.Chrome(executable_path=[path], chrome_options=options)

#検索ワードのリスト
wants = ['a', 'b', 'c']

page = 1

for product in wants: #continue until getting the last page

    browser.get("https://www.mercari.com/jp/search/?sort_order=&keyword={}&category_root=&brand_name=&brand_id=&size_group=&price_min=&price_max=&item_condition_id%5B1%5D=1&item_condition_id%5B2%5D=1&item_condition_id%5B3%5D=1&item_condition_id%5B4%5D=1&status_on_sale=1".format(product))

    header = '\n****************************************************\n検索ワード：' + product
    send_to_slack(header)

    if len(browser.find_elements_by_css_selector("li.pager-next .pager-cell:nth-child(1) a")) > 0:

        posts = browser.find_elements_by_css_selector(".items-box")
        num = 1

        for post in posts:

            #とりあえず最大５件出力
            #本当は15分間の新着だけ出力したかったけど、pc版メルカリでは出品時刻が表示されないので一旦断念
            if num > 5:
                break

            title = post.find_element_by_css_selector("h3.items-box-name").text

            price = post.find_element_by_css_selector(".items-box-price").text
            price = price.replace('¥', '')

            url = post.find_element_by_css_selector("a").get_attribute("href")

            info = 'title: ' + title + '\n' + 'price: ' + price + '\n' + 'url: ' + url + '\n'
            send_to_slack(info)

            num += 1

        page += 1

        btn = browser.find_element_by_css_selector("li.pager-next .pager-cell:nth-child(1) a").get_attribute("href")
        browser.get(btn)

    #次のページがない場合
    elif (len(browser.find_elements_by_css_selector("li.pager-next .pager-cell:nth-child(1) a")) == 0):

        #検索結果が０件
        if browser.find_element_by_css_selector("h2.search-result-head").text == "検索結果 0件":

            message = 'item is not found'
            send_to_slack(message)
            continue

        posts = browser.find_elements_by_css_selector(".items-box")
        num = 1

        for post in posts:

            if num > 5:
                break

            title = post.find_element_by_css_selector("h3.items-box-name").text

            price = post.find_element_by_css_selector(".items-box-price").text
            price = price.replace('¥', '')

            url = post.find_element_by_css_selector("a").get_attribute("href")

            info = 'title: ' + title + '\n' + 'price: ' + price + '\n' + 'url: ' + url + '\n'
            send_to_slack(info)

            num += 1

print("DONE")
