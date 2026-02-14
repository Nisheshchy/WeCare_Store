import datetime
import uuid
import read
import write


DATA_FILE = "product.txt"
BUY_QUANTITY = 3
FREE_QUANTITY = 1
VAT_RATE = 0.13 


def current_time():

        current_time = datetime.datetime.now()
        return (
        str(current_time.year)+"-"
        + str(current_time.month)+"-"
        + str(current_time.day)+" "
        + str(current_time.hour)+":"
        + str(current_time.minute)+":"
        + str(current_time.second)+":"
        + str(current_time.microsecond)
        )

def sale_product():
    try:
        print("\nAvailable Products For Sales:")
        products = read.load_product(DATA_FILE)
        if not products:
            print("No products available for sale.\n")
            return
        
        display_sales(products)
        while True:
            sold_product_id = input("\nEnter the ID of the product for sale (or 'exit' to go back): ")
            if sold_product_id.lower() == 'exit':
                break
                
            if not sold_product_id.isdigit():
                print("Invalid input. Please enter a numeric product ID or 'exit'.\n")
                continue
                
            product_id = int(sold_product_id)
            if product_id not in products:
                print("Invalid product ID. Please enter a valid ID.\n")
                continue
                
            available_quantity = products[product_id]["quantity"]
            if available_quantity <= 0:
                print("The item is out of stock.\n")
                continue
                
            customer_name = input("Enter customer name: ")
            if not customer_name:
                print("Customer name cannot be empty.\n")
                continue
            
            if not customer_name.isalpha():
               print("Invalid input. Please use letters only (no numbers or spaces).\n")
               continue
                
            quantity_to_buy = get_quantity(available_quantity)
            if quantity_to_buy is None:
                continue
                
            free_items = (quantity_to_buy // BUY_QUANTITY) * FREE_QUANTITY
            effective_quantity = quantity_to_buy
            
            if free_items > 0 and available_quantity >= (quantity_to_buy + free_items):
                effective_quantity += free_items
                print(f"Special offer: Buy {BUY_QUANTITY} get {FREE_QUANTITY} free! You get {free_items} free item(s).")
            elif free_items > 0:
                free_items = 0
                print("Not enough stock for the free item offer.")
            
            total_selling_price = calculate_price(products[product_id]["price"]) * quantity_to_buy
            vat_amount = total_selling_price * VAT_RATE
            total_price_with_vat = total_selling_price + vat_amount
            
            try:
                sale_item(products, product_id, customer_name, quantity_to_buy, effective_quantity, free_items, total_selling_price, vat_amount, total_price_with_vat)
                products[product_id]["quantity"] -= effective_quantity
                write.save_product_items(products, DATA_FILE)
            except Exception as e:
                print(f"Error processing sale: {str(e)}")
                continue
                
    except Exception as e:
        print(f"Error in sale_product: {str(e)}")

def restock_product():
    try:
        print("\nAvailable Products For Restock:")
        products = read.load_product(DATA_FILE)
        if not products:
            print("No products available to restock.\n")
            return
            
        display_restock(products)
        
        supplier = input("Enter the supplier name: ")
        if not supplier:
            print("Supplier name cannot be empty.\n")
            return
        # Check if the string contains ONLY letters a-z
        if not supplier.isalpha():
            print("Invalid input: Supplier name must contain only letters (A-Z).\n")
            return
            
        while True:
            print(f"\nSupplier_name: {supplier}")
            item_id = input("Enter the ID of the item to restock (or 'exit' to go back): ")
            if item_id.lower() == 'exit':
                break
                
            if not item_id.isdigit():
                print("Please enter a valid numeric ID or 'exit'.\n")
                continue
                
            product_id = int(item_id)
            if product_id not in products:
                print("Invalid product ID. Please enter a valid ID.\n")
                continue
                
            quantity_to_add = get_quantity_to_add()
            if quantity_to_add is None:
                continue
                
            try:
                total_price = products[product_id]["price"] * quantity_to_add
                products[product_id]["quantity"] += quantity_to_add
                write.save_product_items(products, DATA_FILE)
                print(f"Updated quantity for {products[product_id]['name']}: {products[product_id]['quantity']}")
                print(f"Total Restock Price: ${total_price:.2f}")
                
                invoice = generate_restock_invoice(
                    products[product_id]["name"],
                    products[product_id]["brand"],
                    quantity_to_add,
                    supplier,
                    total_price
                )
                if invoice:
                    invoice_file_name = f"{supplier}_RestockInvoice_{current_time()}.txt"
                    write.save_invoice_to_file(invoice, invoice_file_name)
            except Exception as e:
                print(f"Error processing restock: {str(e)}")
                continue
                
    except Exception as e:
        print(f"Error in restock_product: {str(e)}")

def display_sales(products):
    if not products:
        print("\nNo products available for sale.\n")
        return

    print("\nAvailable Products For Sales:")
    print("-" * 80)
    print(f"{'ID':<8}{'Name':<20}{'Brand':<15}{'Selling Price ($)':<20}{'Quantity':<10}{'Country':<15}")
    print("-" * 80)
    
    for product_id, details in products.items():
        selling_price = calculate_price(details["price"])
        print(f"{product_id:<8}{details['name']:<20}{details['brand']:<15}{selling_price:<20.2f}{details['quantity']:<10}{details['country']:<15}")
    
    print()

def display_restock(products):
    if not products:
        print("\nNo products available for restocking.\n")
        return

    print("\nInventory Restock:")
    print("-" * 80)
    print(f"{'ID':<8}{'Name':<20}{'Brand':<15}{'Quantity':<10}{'Price ($)':<12}{'Country':<15}")
    print("-" * 80)
    
    for product_id, details in products.items():
        print(f"{product_id:<8}{details['name']:<20}{details['brand']:<15}{details['quantity']:<10}{details['price']:<12.2f}{details['country']:<15}")
    
    print()

def get_quantity(available_quantity):

    while True:
        try:
            quantity = int(input(f"Enter the quantity for sale (up to {available_quantity} available): "))
            if quantity <= 0 or quantity > available_quantity:
                print(f"Please enter a quantity between 1 and {available_quantity}.")
            else:
                return quantity
        except ValueError:
            print("Please enter a valid number.")

def get_quantity_to_add():
    while True:
        try:
            quantity = int(input("Enter the quantity to add: "))
            if quantity <= 0:
                print("Please enter a positive number.")
            else:
                return quantity
        except ValueError:
            print("Please enter a valid number.")

def calculate_price(price):

    return price * 2  

def sale_item(products, product_id, customer_name, quantity_to_buy, effective_quantity, free_items, total_selling_price, vat_amount, total_price_with_vat):
    current_time_file = current_time()
    
    print("\nSale Summary:")
    print(f"Sale Date: {current_time_file}")
    print(f"Product ID: {product_id}")
    print(f"Product: {products[product_id]['name']}")
    print(f"Brand: {products[product_id]['brand']}")
    print(f"Customer: {customer_name}")
    print(f"Quantity Sold: {quantity_to_buy}")
    if free_items > 0:
        print(f"(Includes {free_items} free item(s) due to Buy {BUY_QUANTITY} Get {FREE_QUANTITY} Free offer)")
    print(f"Total Selling Price: ${total_selling_price:.2f}")
    print(f"VAT (13%): ${vat_amount:.2f}")
    print(f"Total Price with VAT: ${total_price_with_vat:.2f}")
    
    invoice = generate_invoice(
        customer_name,
        products[product_id]['name'],
        products[product_id]['brand'],
        products[product_id]['country'],
        quantity_to_buy,
        effective_quantity,
        free_items,
        total_selling_price,
        vat_amount,
        total_price_with_vat,
        current_time_file
    )
    invoice_file_name = f"{customer_name}_SaleInvoice_{current_time()}.txt"
    write.save_invoice_to_file(invoice, invoice_file_name)

def generate_invoice(customer_name, product_name, brand, country, quantity_to_buy, effective_quantity, free_items, total_selling_price, vat_amount, total_price_with_vat, current_time_str):
    try:
        invoice_id = str(uuid.uuid4())[:8]  
        invoice = f"""
------------------------------------------------------
     WeCare System For Sales Invoice
------------------------------------------------------
Invoice ID: {invoice_id}
Sale Date: {current_time_str}
Customer Name: {customer_name}
Product Name: {product_name}
Brand: {brand}
Country: {country}
Quantity Sold: {quantity_to_buy}
Free Items: {free_items}
Total Quantity: {effective_quantity}
"""
        if free_items > 0:
            invoice += f"(Includes {free_items} free item(s) due to Buy {BUY_QUANTITY} Get {FREE_QUANTITY} Free offer)\n"
        invoice += f"Total Selling Price: ${total_selling_price:.2f}\n"
        invoice += f"VAT (13%): ${vat_amount:.2f}\n"
        invoice += f"Total Price with VAT: ${total_price_with_vat:.2f}\n"
        invoice += "------------------------------------------------------\nThank you!\n"
        return invoice
    except Exception as e:
        print(f"Error generating invoice: {str(e)}")
        return None

def generate_restock_invoice(item_name, item_brand, quantity_added, supplier, total_price):
    try:
        current_time_file = current_time()
        invoice_id = str(uuid.uuid4())[:8] 
        
        invoice = f"""
------------------------------------------------------
     WeCare System For Restocks Invoice
------------------------------------------------------
Invoice ID: {invoice_id}
Restock Date: {current_time_file}
Product: {item_name}
Brand: {item_brand}
Supplier Name: {supplier}
Total Quantity Added: {quantity_added}
Total Restock Price: ${total_price:.2f}
------------------------------------------------------
\tThank you!\n
"""
        return invoice
    except Exception as e:
        print(f"Error generating restock invoice: {str(e)}")
        return None

def add_product():
    print("\nAdd a New Product:")
    products = read.load_product(DATA_FILE)
    
    name = input("Enter product name: ")
    if not name:
        print("Product name cannot be empty.\n")
        return
    if any(details["name"].lower() == name.lower() for details in products.values()):
        print("A product with this name already exists.\n")
        return
    brand = input("Enter product brand: ")
    if not brand:
        print("Brand cannot be empty.\n")
        return
    while True:
        try:
            quantity = int(input("Enter the quantity of product: "))
            if quantity < 0:
                print("Quantity cannot be negative.")
            else:
                break
        except ValueError:
            print("Please enter a valid number.")
    
    while True:
        try:
            price = float(input("Enter product price: "))
            if price <= 0:
                print("Price must be positive.")
            else:
                break
        except ValueError:
            print("Please enter a valid number.")
    
    country = input("Enter country of origin: ")
    if not country:
        print("Country cannot be empty.\n")
        return
    
    product_id = len(products) + 1
    products[product_id] = {
        "name": name,
        "brand": brand,
        "quantity": quantity,
        "price": price,
        "country": country
    }
    
    write.save_product_items(products, DATA_FILE)
    print(f"\nProduct '{name}' added successfully with ID {product_id}.")