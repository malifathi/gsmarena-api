#!/usr/bin/env python3
"""
Basic usage examples for GSMArena API Python version
"""

import gsmarena
import json
import time


def print_json(data, title="Result"):
    """Helper function to print JSON data nicely"""
    print(f"\n{title}:")
    print(json.dumps(data, indent=2))


def main():
    """Demonstrate basic usage of all API features"""
    
    print("=== GSMArena API Python - Basic Usage Examples ===")
    
    try:
        # 1. Get all brands
        print("\n1. Getting all brands...")
        brands = gsmarena.catalog.get_brands()
        print(f"Found {len(brands)} brands")
        # Show first 3 brands
        print_json(brands[:3], "First 3 brands")
        
        # 2. Get devices for Apple brand
        print("\n2. Getting Apple devices...")
        apple_brand = next((b for b in brands if 'apple' in b['name'].lower()), None)
        if apple_brand:
            print(f"Getting devices for {apple_brand['name']} (ID: {apple_brand['id']})")
            apple_devices = gsmarena.catalog.get_brand(apple_brand['id'])
            print(f"Found {len(apple_devices)} Apple devices")
            # Show first 3 devices
            print_json(apple_devices[:3], "First 3 Apple devices")
            
            # 3. Get detailed specs for first Apple device
            if apple_devices:
                device = apple_devices[0]
                print(f"\n3. Getting detailed specs for {device['name']}...")
                device_specs = gsmarena.catalog.get_device(device['id'])
                print_json({
                    'name': device_specs['name'],
                    'img': device_specs['img'],
                    'quickSpec': device_specs['quickSpec'][:3]  # Show first 3 quick specs
                }, f"Specs for {device['name']}")
        
        # Small delay to be respectful to the server
        time.sleep(1)
        
        # 4. Search for devices
        print("\n4. Searching for 'samsung galaxy' devices...")
        search_results = gsmarena.search.search('samsung galaxy')
        print(f"Found {len(search_results)} results")
        print_json(search_results[:3], "First 3 search results")
        
        time.sleep(1)
        
        # 5. Get top devices
        print("\n5. Getting top devices...")
        top_devices = gsmarena.top.get()
        print(f"Found {len(top_devices)} top categories")
        if top_devices:
            print_json(top_devices[0], "First top category")
        
        time.sleep(1)
        
        # 6. Get current deals
        print("\n6. Getting current deals...")
        deals = gsmarena.deals.get_deals()
        print(f"Found {len(deals)} deals")
        if deals:
            # Show first deal with simplified info
            deal = deals[0]
            simplified_deal = {
                'name': deal['name'],
                'price': f"{deal['deal']['currency']} {deal['deal']['price']}",
                'discount': f"{deal['deal']['discount']}%",
                'memory': deal['deal']['memory']
            }
            print_json(simplified_deal, "First deal")
        
        time.sleep(1)
        
        # 7. Get glossary terms
        print("\n7. Getting glossary terms...")
        glossary = gsmarena.glossary.get()
        print(f"Found glossary with {len(glossary)} letter categories")
        # Show first letter category
        if glossary:
            print_json(glossary[0], "First glossary category")
            
            # 8. Get detailed definition for first term
            if glossary[0]['list']:
                term = glossary[0]['list'][0]
                print(f"\n8. Getting definition for '{term['name']}'...")
                term_detail = gsmarena.glossary.get_term(term['id'])
                print_json({
                    'title': term_detail['title'],
                    'html_length': len(term_detail['html'])
                }, f"Definition for {term['name']}")
    
    except Exception as e:
        print(f"Error occurred: {e}")
        print("This might be due to network issues or changes in GSMArena's website structure.")


if __name__ == "__main__":
    main()