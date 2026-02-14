def load_product(file_path):
    products = {}
    try:
        with open(file_path, "r") as file:
            line_number = 0
            for line in file:
                line_number += 1
                line = line.strip()
                if not line:
                    continue
                values = line.split(",")
                if len(values) < 5:
                    print(f"Warning: Skipping line {line_number} in {file_path}: {line}")
                    continue
                try:
                    product_id = len(products) + 1
                    name = values[0].strip()
                    brand = values[1].strip()
                    quantity = int(values[2].strip())
                    price = float(values[3].strip())
                    country = values[4]

                    products[product_id] = {
                        "name": name,
                        "brand": brand,
                        "quantity": quantity,
                        "price": price,
                        "country": country
                    }
                except (ValueError, IndexError) as e:
                    print(f"Error parsing line {line_number} in {file_path}: {e}")
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return products

def display_products():
    print("-" * 80)
    print("\nWeCare Store Inventory")
    products = load_product("product.txt")
    if not products:
        print("No products available.\n")
        return
    print("-" * 80)
    print(f"{'ID':<5}{'Name':<20}{'Brand':<15}{'Quantity':<10}{'Price ($)':<12}{'Country':<15}")
    print("-" * 80)
    
    for product_id, details in products.items():
        print(f"{product_id:<5}{details['name']:<20}{details['brand']:<15}{details['quantity']:<10}{details['price']:<12.2f}{details['country']:<15}")
    
    print()