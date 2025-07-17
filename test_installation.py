#!/usr/bin/env python3
"""
Simple test script to verify GSMArena API Python installation
"""

import sys
import time

def test_imports():
    """Test if all modules can be imported"""
    try:
        import gsmarena
        from gsmarena import catalog, search, deals, top, glossary
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality with simple requests"""
    try:
        import gsmarena
        
        print("\nTesting basic functionality...")
        
        # Test 1: Get brands (should return a list)
        print("- Testing catalog.get_brands()...")
        brands = gsmarena.catalog.get_brands()
        if isinstance(brands, list) and len(brands) > 0:
            print(f"  ✓ Got {len(brands)} brands")
        else:
            print("  ✗ Failed to get brands or empty result")
            return False
        
        time.sleep(1)  # Be respectful to the server
        
        # Test 2: Search (should return a list)
        print("- Testing search.search()...")
        search_results = gsmarena.search.search('apple')
        if isinstance(search_results, list):
            print(f"  ✓ Got {len(search_results)} search results for 'apple'")
        else:
            print("  ✗ Failed to get search results")
            return False
        
        time.sleep(1)
        
        # Test 3: Get glossary (should return a list, might be empty due to website changes)
        print("- Testing glossary.get()...")
        glossary = gsmarena.glossary.get()
        if isinstance(glossary, list):
            print(f"  ✓ Got glossary with {len(glossary)} letter categories (empty is OK)")
        else:
            print("  ✗ Failed to get glossary - not a list")
            return False
        
        print("\n✓ All basic functionality tests passed")
        return True
        
    except Exception as e:
        print(f"✗ Error during functionality test: {e}")
        return False

def main():
    """Run all tests"""
    print("=== GSMArena API Python - Installation Test ===")
    
    # Test imports
    if not test_imports():
        print("\nInstallation test FAILED: Import errors")
        sys.exit(1)
    
    # Test basic functionality
    try:
        if not test_basic_functionality():
            print("\nInstallation test FAILED: Functionality errors")
            sys.exit(1)
    except Exception as e:
        print(f"\nInstallation test FAILED: {e}")
        print("This might be due to network issues or changes in GSMArena's website.")
        sys.exit(1)
    
    print("\n🎉 Installation test PASSED! GSMArena API Python is working correctly.")
    print("\nYou can now use the library in your projects:")
    print("  import gsmarena")
    print("  brands = gsmarena.catalog.get_brands()")

if __name__ == "__main__":
    main()