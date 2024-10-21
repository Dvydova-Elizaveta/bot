import requests
from bs4 import BeautifulSoup



def search_yandex_market(query):
    query = query.replace(' ', '+')
    url = f"https://market.yandex.ru/search?text={query}"

    response = requests.get(url)

    if response.status_code != 200:
        return "Ошибка при подключении к Яндекс Маркету."

    soup = BeautifulSoup(response.text, 'html.parser')

    # Проверяем, есть ли элементы товаров на странице
    items = soup.find_all('div', {'data-apiary-widget-name': '@marketfront/SerpEntity'})


    results = []

    for item in items[:3]:  # Берем только 5 товаров
        # Название товара
        title_tag = item.find('span', {'data-auto': 'snippet-title'})
        title = title_tag.text.strip() if title_tag else 'Название не найдено'

        # Ссылка на товар
        link_tag = item.find('a', {'data-auto': 'snippet-link'})
        link = link_tag.get('href')
        # Цена товара
        price_tag = item.find('span', {'data-auto': 'snippet-price-current'})
        price = price_tag.text.strip() if price_tag else 'Цена не найдена'

        results.append({
            'title': title,
            'link': link,
            'price': price
        })

    return results if results else "Не удалось найти товары по запросу."


# Пример использования функции
query = "ноутбук"
items = search_yandex_market(query)

if isinstance(items, list):
    for item in items:
        print(f"Название: {item['title']}\nЦена: {item['price']}\nСсылка: {item['link']}\n")
else:
    print(items)
