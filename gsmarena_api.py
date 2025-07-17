import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = 'https://www.gsmarena.com/'


def get_html(path):
    url = urljoin(BASE_URL, path)
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.text


def get_brands():
    html = get_html('makers.php3')
    soup = BeautifulSoup(html, 'html.parser')
    brands = []
    for td in soup.select('table td'):
        a = td.find('a')
        if not a:
            continue
        brand_id = a['href'].replace('.php', '')
        name = a.text.replace(' devices', '').strip('0123456789 ')
        devices = int(td.find('span').text.replace(' devices', ''))
        brands.append({'id': brand_id, 'name': name, 'devices': devices})
    return brands


def get_brand_devices(brand_id):
    devices = []
    next_path = f'{brand_id}.php'
    while next_path:
        html = get_html(next_path)
        soup = BeautifulSoup(html, 'html.parser')
        for li in soup.select('.makers li'):
            a = li.find('a')
            img = li.find('img')
            devices.append({
                'id': a['href'].replace('.php', ''),
                'name': li.find('span').text,
                'img': img['src'] if img else None,
                'description': img['title'] if img and img.has_attr('title') else None
            })
        next_link = soup.select_one('a.prevnextbutton[title="Next page"]')
        if next_link:
            next_path = next_link['href']
        else:
            next_path = None
    return devices


def get_device_details(device_id):
    html = get_html(f'{device_id}.php')
    soup = BeautifulSoup(html, 'html.parser')
    quick_spec = [
        {'name': 'Display size', 'value': soup.select_one('span[data-spec=displaysize-hl]').text if soup.select_one('span[data-spec=displaysize-hl]') else ''},
        {'name': 'Display resolution', 'value': soup.select_one('div[data-spec=displayres-hl]').text if soup.select_one('div[data-spec=displayres-hl]') else ''},
        {'name': 'Camera pixels', 'value': soup.select_one('.accent-camera').text if soup.select_one('.accent-camera') else ''},
        {'name': 'Video pixels', 'value': soup.select_one('div[data-spec=videopixels-hl]').text if soup.select_one('div[data-spec=videopixels-hl]') else ''},
        {'name': 'RAM size', 'value': soup.select_one('.accent-expansion').text if soup.select_one('.accent-expansion') else ''},
        {'name': 'Chipset', 'value': soup.select_one('div[data-spec=chipset-hl]').text if soup.select_one('div[data-spec=chipset-hl]') else ''},
        {'name': 'Battery size', 'value': soup.select_one('.accent-battery').text if soup.select_one('.accent-battery') else ''},
        {'name': 'Battery type', 'value': soup.select_one('div[data-spec=battype-hl]').text if soup.select_one('div[data-spec=battype-hl]') else ''},
    ]
    name = soup.select_one('.specs-phone-name-title').text if soup.select_one('.specs-phone-name-title') else ''
    img = soup.select_one('.specs-photo-main a img')['src'] if soup.select_one('.specs-photo-main a img') else None
    detail_spec = []
    for table in soup.find_all('table'):
        category = table.find('th').text if table.find('th') else ''
        spec_list = []
        for tr in table.find_all('tr'):
            ttl = tr.find('td', class_='ttl')
            nfo = tr.find('td', class_='nfo')
            if ttl and nfo:
                spec_list.append({'name': ttl.text, 'value': nfo.text})
        if category:
            detail_spec.append({'category': category, 'specifications': spec_list})
    return {
        'name': name,
        'img': img,
        'detailSpec': detail_spec,
        'quickSpec': quick_spec
    }


def search(query):
    html = get_html(f'results.php3?sQuickSearch=yes&sName={query}')
    soup = BeautifulSoup(html, 'html.parser')
    results = []
    for li in soup.select('.makers li'):
        a = li.find('a')
        img = li.find('img')
        name = li.find('span').decode_contents().replace('<br>', ' ')
        results.append({
            'id': a['href'].replace('.php', ''),
            'name': name,
            'img': img['src'] if img else None,
            'description': img['title'] if img and img.has_attr('title') else None
        })
    return results