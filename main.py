import operations
import read

def main():
    print("-"*50)
    print("\tWelcome to WeCare Store")
    print("-" * 50)
    
    while True:
        print("\nWhich option do you like to choose:")  
        print("(1) Display all the Items")
        print("(2) Sale an Items")  
        print("(3) Restock an Item")  
        print("(4) Add the new Items")
        print("(5) Exit\n")
        print("-"*50)
        option = input("Enter the own choice (1-5): ")  
        
        if option == '1':
            read.display_products()
            
        elif option == '2':
            operations.sale_product()
            
        elif option == '3':
            operations.restock_product()
        elif option == '4':
            operations.add_product()
            
        elif option == '5':
            print("\nThank you for Visiting Us!")
            print("-" * 50)
            break
            
        else:
            print("Enter a valid option (1-5)\n")  

if __name__ == '__main__':
    main()