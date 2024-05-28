import requests
import os

jina_reader_key = os.getenv('JINA_READER_KEY')
headers = {
        "X-With-Generated-Alt": "true"
    }
if jina_reader_key:
    headers['Authorization'] = f'Bearer {jina_reader_key}'


def get_jina(page_url):
    def get_main_article(jina_md):
        return jina_md.split('回覆')[0]
    
    page_url = 'https://r.jina.ai/' + page_url
    
    response = requests.get(page_url, headers=headers)
    text = get_main_article(response.text)
    # text = response.text
    return text

def save_crawler_data(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(data)

if __name__ == '__main__':
    page_url = 'https://forum.gamer.com.tw/C.php?bsn=74934&snA=391'
    jina_page = get_jina(page_url)
    save_crawler_data(jina_page, '391.md')
    # print(jina_pages)