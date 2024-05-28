import requests
from bs4 import BeautifulSoup
import os
import tqdm

from get_jina_parse import get_jina, save_crawler_data

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def search(topic_bsn, question):
    response = requests.get(f'https://forum.gamer.com.tw/search.php?bsn={topic_bsn}&q={question}', headers=headers)
    text = response.text

    soup = BeautifulSoup(text, 'html.parser')
    search_results = soup.select('.search-result_article')

    parse_result = []
    for result in search_results:
        title = result.select_one('.search-result_title').text.strip()
        link = result.select_one('.search-result_title a')['href']
        text = result.select_one('.search-result_text').text.strip()
        info = result.select_one('.forum-textinfo').text.strip()
        
        # print('標題:', title)
        # print('連結:', link)
        # print('內文:', text)
        # print('資訊:', info)
        # print('-'*50)
        parse_result.append({
            'title': title,
            'link': link,
            'text': text,
            'info': info
        })

    return parse_result

def search_and_save(topic_bsn, question):
    search_result = search(topic_bsn, question)
    if not search_result:
        print('查無結果')
        return()
    os.makedirs(f'result/{topic_bsn}_{question}', exist_ok=True)

    for i, result in enumerate(tqdm.tqdm(search_result)):
        result_link = result['link']
        # result_title = result['title']
        # result_title = result_title.replace('/', '_')
        # result_title = result_title.replace('\\', '_')
        # result_title = result_title.replace('?', '_')
        jina_page = get_jina(result_link)
        save_crawler_data(jina_page, f'result/{topic_bsn}_{question}/{i}.md')

if __name__ == '__main__':
    topic_bsn = '74934'
    question = '角色'
    search_and_save(topic_bsn, question)