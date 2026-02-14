def save_product_items(products, file_path):

        with open(file_path, "w") as file:
            for details in products.values():
                line = f"{details['name']},{details['brand']},{details['quantity']},{details['price']},{details['country']}\n"
                file.write(line)


def save_invoice_to_file(invoice, file_name):

        with open(file_name, "w") as file:
            file.write(invoice)
        print(f"Invoice generated: Your invoice is saved in {file_name} file\n")
