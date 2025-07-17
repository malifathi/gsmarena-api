# GSMArena API - Python Version

GSMArena phone specification and finder - Python port of the original Node.js library. This project is a complete Python implementation that provides the same functionality as the JavaScript version.

The API reads from the GSMArena website and returns JSON data.

## Table of Contents

* [Implemented Features](#implemented-features)
* [Installation](#installation)
* [Usage](#usage)
* [API Reference](#api-reference)
* [Examples](#examples)
* [Requirements](#requirements)
* [License](#license)

## Implemented Features

- [x] Get all brands
- [x] Get devices by brand
- [x] Get device specification
- [x] Find devices by keyword
- [x] Top of devices
- [x] Hot deals
- [x] Glossary
- [x] Glossary detail
- [ ] Find devices by advanced filters
- [ ] News
- [ ] Reviews

## Installation

### Using pip (recommended)

```bash
pip install gsmarena-api-python
```

### From source

```bash
git clone https://github.com/your-username/gsmarena-api-python.git
cd gsmarena-api-python
pip install -r requirements.txt
pip install -e .
```

## Usage

### Import

```python
import gsmarena

# Or import specific modules
from gsmarena import catalog, search, deals, top, glossary
```

### Brand list

```python
brands = gsmarena.catalog.get_brands()
print(brands)
```

```json
[
  {
    "id": "apple-phones-48",
    "name": "Apple",
    "devices": 98
  }
]
```

### Device list by brand

```python
devices = gsmarena.catalog.get_brand('apple-phones-48')
print(devices)
```

```json
[
  {
    "id": "apple_iphone_13_pro_max-11089",
    "name": "iPhone 13 Pro Max",
    "img": "https://fdn2.gsmarena.com/vv/bigpic/apple-iphone-13-pro-max.jpg",
    "description": "Apple iPhone 13 Pro Max smartphone. Announced Sep 2021..."
  }
]
```

### Device detail

```python
device = gsmarena.catalog.get_device('apple_iphone_13_pro_max-11089')
print(device)
```

```json
{
  "name": "Apple iPhone 13 Pro Max",
  "img": "https://fdn2.gsmarena.com/vv/bigpic/apple-iphone-13-pro-max.jpg",
  "quickSpec": [
    {
      "name": "Display size",
      "value": "6.7\""
    }
  ],
  "detailSpec": [
    {
      "category": "Network",
      "specifications": [
        {
          "name": "Technology",
          "value": "GSM / CDMA / HSPA / EVDO / LTE / 5G"
        }
      ]
    }
  ]
}
```

### Searching for device

```python
devices = gsmarena.search.search('casio')
print(devices)
```

```json
[
  {
    "id": "casio_g_zone_ca_201l-5384",
    "name": "Casio G'zOne CA-201L",
    "img": "https://fdn2.gsmarena.com/vv/bigpic/casio-gzone-ca-201l.jpg",
    "description": "Casio G'zOne CA-201L Android smartphone. Announced Mar 2013..."
  }
]
```

### Top

```python
top_devices = gsmarena.top.get()
print(top_devices)
```

```json
[
  {
    "category": "Top 10 by daily interest",
    "list": [
      {
        "position": 1,
        "id": "xiaomi_12-11285",
        "name": "Xiaomi 12",
        "dailyHits": 50330
      }
    ]
  }
]
```

### Deals

```python
deals = gsmarena.deals.get_deals()
print(deals)
```

```json
[
  {
    "id": "oneplus_9-10747",
    "img": "https://m.media-amazon.com/images/I/31ICm7rK-hS._SL500_.jpg",
    "url": "https://www.amazon.co.uk/dp/B08V1NKHZF?tag=gsmcom-21&linkCode=osi&th=1&psc=1",
    "name": "OnePlus 9",
    "description": "OnePlus 9 5G (UK) SIM-Free Smartphone with Hasselblad Camera for Mobile - Arctic Sky...",
    "deal": {
      "memory": "128GB 8GB RAM",
      "storeImg": "https://fdn.gsmarena.com/imgroot/static/stores/amazon-uk1.png",
      "price": 449.00,
      "currency": "£",
      "discount": 24.6
    },
    "history": [
      {
        "time": "Previous",
        "price": 479.00,
        "currency": "£"
      }
    ]
  }
]
```

### Glossary

```python
glossary_terms = gsmarena.glossary.get()
print(glossary_terms)
```

```json
[
  {
    "letter": "X",
    "list": [
      {
        "id": "xenon-flash",
        "name": "Xenon flash"
      }
    ]
  }
]
```

### Glossary detail

```python
term = gsmarena.glossary.get_term('xenon-flash')
print(term)
```

```json
{
  "title": "Xenon flash - definition",
  "html": "<p>A xenon flash produces an extremely intense full-spectrum white...</p>"
}
```

## API Reference

### Catalog

- `catalog.get_brands()` - Get all available brands
- `catalog.get_brand(brand_id)` - Get devices for a specific brand
- `catalog.get_device(device_id)` - Get detailed specifications for a device

### Search

- `search.search(keyword)` - Search for devices by keyword

### Deals

- `deals.get_deals()` - Get current device deals and pricing

### Top

- `top.get()` - Get top devices rankings

### Glossary

- `glossary.get()` - Get all glossary terms organized by letter
- `glossary.get_term(term_id)` - Get detailed definition for a specific term

## Examples

Check the `examples/` directory for more detailed usage examples:

- `basic_usage.py` - Basic API usage examples
- `device_comparison.py` - Compare multiple devices
- `brand_analysis.py` - Analyze devices by brand

## Requirements

- Python 3.7+
- requests >= 2.31.0
- beautifulsoup4 >= 4.12.0
- lxml >= 4.9.0

## Error Handling

The library includes basic error handling for HTTP requests. If a request fails, it will raise a `requests.RequestException`. You should handle these exceptions in your code:

```python
import gsmarena
import requests

try:
    brands = gsmarena.catalog.get_brands()
except requests.RequestException as e:
    print(f"Error fetching data: {e}")
```

## Rate Limiting

Please be respectful when using this API. GSMArena is a third-party service, so avoid making too many requests in a short period to prevent being rate-limited or blocked.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is MIT licensed, same as the original Node.js version.

## Differences from Node.js Version

This Python port maintains the same API structure and return formats as the original Node.js version, with the following adaptations:

1. Uses Python naming conventions (snake_case for methods)
2. Includes type hints for better code documentation
3. Uses Python-specific libraries (requests, BeautifulSoup)
4. Provides proper Python package structure

## Acknowledgments

This is a Python port of the original [gsmarena-api](https://github.com/nordmarin/gsmarena-api) Node.js library created by [@nordmarin](https://t.me/nordmarin).