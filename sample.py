import os
from time import sleep
from clicknium import clicknium as cc, locator, ui
import requests
import math

search_key_word = 'boots'

def main():
    # open website
    tab = cc.chrome.open("https://www.bornshoes.com/")

    # input search keyword and click the search button
    tab.find_element(locator.bornshoes.btn_search).click()
    tab.find_element(locator.bornshoes.txt_search).set_text(search_key_word)
    tab.find_element(locator.bornshoes.btn_do_search).click()

    # wait the page loading
    sleep(4)

    # set filter 
    tab.find_element(locator.bornshoes.select_item).select_item('SORT: Most Popular')
    sleep(4)

    # get page size and calc the page count
    page_size = tab.find_element(locator.bornshoes.div_page_size).get_text().split(' ')[1]
    all_count = tab.find_element(locator.bornshoes.btn_show_all).get_text().split('(')[1].split(')')[0]
    page_count = math.ceil(  int(all_count)/int(page_size))
    print(f'page_size is :{page_size},all_count is :{all_count}, page_count is :{page_count}')
    
    # load all items of top 5 pages
    if(page_count > 5):
        page_count = 5
    for x in range(0,page_count-1):
        tab.find_element(locator.bornshoes.btn_show_more).click()
        sleep(4)
    
    # find the similar elements
    similar_elements_img = tab.find_elements(locator.bornshoes.similar_img)
    similar_elements_prices = tab.find_elements(locator.bornshoes.similar_price)
    print(f'similar_elements_img count:{len(similar_elements_img)},similar_elements_prices count:{len(similar_elements_prices)}')
    
    index = 0
    for img in similar_elements_img:
        img1 = img.children[0]
        download_img(img1,index)
        
        index+=1

    sleep(3)
    tab.close()
    

def download_img(img_obj,index):
    
    img_src = img_obj.get_property('src')
    print(f'index:{index},start download: {img_src}...')
    
    # img = requests.get(img_src, 
    #                 proxies=dict(http='socks5://127.0.0.1:10808',
    #                              https='socks5://127.0.0.1:10808'))

    img = requests.get(img_src)

    filepath = './download/'+img_src.split('?')[0].split('/')[-1]
    i = 1
    while(os.path.exists(filepath)):
        filepath = f'./download/{img_src.split("?")[0].split("/")[-1].split(".")[0]}-{i}.jpg'
        i+=1
    with open(filepath,'wb') as f:
        f.write(img.content)
    print(f'index:{index},download success!')

if __name__ == "__main__":
    main()
    
