# GSMArena API (Python)

A simple Python wrapper for scraping phone data from [GSMArena](https://www.gsmarena.com/).

## Features
- Get all brands
- Get all devices for a brand
- Get device details
- Search for devices

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from gsmarena_api import get_brands, get_brand_devices, get_device_details, search

# Get all brands
brands = get_brands()
print(brands)

# Get all devices for a brand
samsung_devices = get_brand_devices('samsung')
print(samsung_devices)

# Get details for a specific device
device = get_device_details('samsung_galaxy_s24_ultra_5g-12024')
print(device)

# Search for devices
results = search('iphone 15')
print(results)
```

## Notes
- This project scrapes GSMArena and may break if the site layout changes.
- Use responsibly and do not overload GSMArena with requests.
