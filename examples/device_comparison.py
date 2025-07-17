#!/usr/bin/env python3
"""
Device comparison example for GSMArena API Python version
Compare specifications between multiple devices
"""

import gsmarena
import json
import time
from typing import List, Dict, Any


def get_key_specs(device_specs: Dict[str, Any]) -> Dict[str, str]:
    """Extract key specifications from device specs"""
    key_specs = {}
    
    # Get quick specs
    for spec in device_specs.get('quickSpec', []):
        key_specs[spec['name']] = spec['value']
    
    # Extract some important detailed specs
    for category in device_specs.get('detailSpec', []):
        if category['category'].lower() == 'platform':
            for spec in category['specifications']:
                if 'os' in spec['name'].lower():
                    key_specs['Operating System'] = spec['value']
                elif 'chipset' in spec['name'].lower():
                    key_specs['Chipset'] = spec['value']
        
        elif category['category'].lower() == 'memory':
            for spec in category['specifications']:
                if 'internal' in spec['name'].lower():
                    key_specs['Internal Storage'] = spec['value']
    
    return key_specs


def compare_devices(device_ids: List[str]) -> None:
    """Compare multiple devices by their specifications"""
    
    print(f"=== Comparing {len(device_ids)} Devices ===")
    
    devices_data = []
    
    # Fetch specs for each device
    for device_id in device_ids:
        try:
            print(f"\nFetching specs for device: {device_id}")
            specs = gsmarena.catalog.get_device(device_id)
            key_specs = get_key_specs(specs)
            
            devices_data.append({
                'id': device_id,
                'name': specs['name'],
                'specs': key_specs
            })
            
            # Be respectful to the server
            time.sleep(1)
            
        except Exception as e:
            print(f"Error fetching specs for {device_id}: {e}")
    
    if not devices_data:
        print("No device data could be fetched for comparison.")
        return
    
    # Print comparison table
    print("\n" + "="*100)
    print("DEVICE COMPARISON")
    print("="*100)
    
    # Print device names
    print(f"{'Specification':<25}", end="")
    for device in devices_data:
        print(f"{device['name'][:20]:<25}", end="")
    print()
    
    print("-" * 100)
    
    # Get all unique spec names
    all_specs = set()
    for device in devices_data:
        all_specs.update(device['specs'].keys())
    
    # Print each specification
    for spec_name in sorted(all_specs):
        print(f"{spec_name:<25}", end="")
        for device in devices_data:
            value = device['specs'].get(spec_name, 'N/A')
            # Truncate long values
            if len(value) > 20:
                value = value[:17] + "..."
            print(f"{value:<25}", end="")
        print()
    
    print("-" * 100)


def find_and_compare_brand_devices(brand_name: str, max_devices: int = 3) -> None:
    """Find devices from a brand and compare them"""
    
    print(f"\n=== Finding and Comparing {brand_name} Devices ===")
    
    # Get all brands
    brands = gsmarena.catalog.get_brands()
    target_brand = None
    
    for brand in brands:
        if brand_name.lower() in brand['name'].lower():
            target_brand = brand
            break
    
    if not target_brand:
        print(f"Brand '{brand_name}' not found.")
        return
    
    print(f"Found brand: {target_brand['name']} with {target_brand['devices']} devices")
    
    # Get devices for the brand
    try:
        devices = gsmarena.catalog.get_brand(target_brand['id'])
        print(f"Fetched {len(devices)} devices")
        
        if len(devices) == 0:
            print("No devices found for this brand.")
            return
        
        # Take first few devices for comparison
        selected_devices = devices[:max_devices]
        device_ids = [device['id'] for device in selected_devices]
        
        print(f"\nSelected devices for comparison:")
        for device in selected_devices:
            print(f"- {device['name']}")
        
        # Compare the devices
        compare_devices(device_ids)
        
    except Exception as e:
        print(f"Error fetching devices for {target_brand['name']}: {e}")


def search_and_compare(search_term: str, max_devices: int = 3) -> None:
    """Search for devices and compare them"""
    
    print(f"\n=== Searching and Comparing: '{search_term}' ===")
    
    try:
        # Search for devices
        search_results = gsmarena.search.search(search_term)
        print(f"Found {len(search_results)} devices matching '{search_term}'")
        
        if len(search_results) == 0:
            print("No devices found for this search term.")
            return
        
        # Take first few devices for comparison
        selected_devices = search_results[:max_devices]
        device_ids = [device['id'] for device in selected_devices]
        
        print(f"\nSelected devices for comparison:")
        for device in selected_devices:
            print(f"- {device['name']}")
        
        # Compare the devices
        compare_devices(device_ids)
        
    except Exception as e:
        print(f"Error searching for '{search_term}': {e}")


def main():
    """Main function to demonstrate device comparison"""
    
    print("=== GSMArena API Python - Device Comparison Examples ===")
    
    # Example 1: Compare specific iPhone models
    print("\n1. Comparing specific iPhone models...")
    iphone_ids = [
        'apple_iphone_15_pro_max-12548',
        'apple_iphone_15_pro-12547',
        'apple_iphone_15-12545'
    ]
    compare_devices(iphone_ids)
    
    time.sleep(2)
    
    # Example 2: Find and compare Samsung devices
    find_and_compare_brand_devices('Samsung', max_devices=3)
    
    time.sleep(2)
    
    # Example 3: Search and compare gaming phones
    search_and_compare('gaming phone', max_devices=2)


if __name__ == "__main__":
    main()