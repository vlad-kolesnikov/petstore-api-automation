#!/usr/bin/env python3
"""
Generate Postman Collections from all test files
Creates both individual collections and one combined collection
"""

import json
from pathlib import Path
from datetime import datetime
from convert_to_postman import PostmanConverter


def generate_combined_collection(test_files: list) -> dict:
    """Generate a single combined Postman collection from multiple test files"""

    combined = {
        "info": {
            "name": "Petstore API - Complete Test Suite",
            "description": f"Complete API test collection with all endpoints\nGenerated: {datetime.now().isoformat()}\n\nIncludes:\n- Pet Operations (CRUD, Search)\n- Store Operations (Orders, Inventory)\n- User Operations (CRUD, Authentication)",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": []
    }

    # Category mapping for better organization
    categories = {
        "pet": "Pet Operations",
        "store": "Store Operations",
        "user": "User Operations"
    }

    # Group items by category
    category_items = {cat: [] for cat in categories.values()}

    for test_file in test_files:
        converter = PostmanConverter(str(test_file))
        collection = converter.convert()

        # Determine category from path
        category_key = test_file.parent.name
        category_name = categories.get(category_key, "Other")

        # Add all folders from this collection
        for item in collection['item']:
            category_items[category_name].append(item)

    # Build final structure with category folders
    for category_name, items in category_items.items():
        if items:
            category_folder = {
                "name": category_name,
                "item": items,
                "description": f"All {category_name.lower()} endpoints"
            }
            combined['item'].append(category_folder)

    return combined


def main():
    """Generate all Postman collections"""

    # Create output directory
    output_dir = Path("postman_collections")
    output_dir.mkdir(exist_ok=True)

    # Find all test JSON files
    test_files = sorted(Path("tests").rglob("*.json"))

    print("=" * 70)
    print("  Generating Postman Collections")
    print("=" * 70)
    print()

    # Generate individual collections
    print("Generating individual collections...")
    individual_collections = []

    for test_file in test_files:
        converter = PostmanConverter(str(test_file))
        output_name = f"postman_{test_file.stem}.json"
        output_path = output_dir / output_name

        converter.save(str(output_path))
        individual_collections.append(output_name)
        print(f"  [OK] {output_name}")

    print()

    # Generate combined collection
    print("Generating combined collection...")
    combined = generate_combined_collection(test_files)
    combined_path = output_dir / "Petstore_API_Complete.json"

    with open(combined_path, 'w', encoding='utf-8') as f:
        json.dump(combined, f, indent=2)

    # Calculate stats
    total_requests = 0
    total_folders = len(combined['item'])

    for category in combined['item']:
        for folder in category['item']:
            total_requests += len(folder['item'])

    print(f"  [OK] Petstore_API_Complete.json")
    print()

    # Summary
    print("=" * 70)
    print("  Summary")
    print("=" * 70)
    print()
    print(f"Individual Collections: {len(individual_collections)}")
    for name in individual_collections:
        print(f"  - {name}")
    print()
    print(f"Combined Collection: Petstore_API_Complete.json")
    print(f"  Categories: {len(combined['item'])}")
    print(f"  Folders: {total_folders}")
    print(f"  Total Requests: {total_requests}")
    print()
    print("All collections saved to: postman_collections/")
    print()
    print("Import into Postman:")
    print("  File -> Import -> Upload Files -> postman_collections/Petstore_API_Complete.json")
    print()


if __name__ == '__main__':
    main()
