import os
import ContentFilter

filter = ContentFilter.Filter()

while True:
        print("1) Block URL")
        print("2) Remove Blocked URL")
        print("3) Exit\n")

        n = input("Option: ")

        if n.isnumeric():
            n = int(n)

            if n == 1:
                url = input("Enter URL: ")
                filter.Add_url(url)
            elif n == 2:
                url = input("Enter URL: ")
                filter.remove_url(url)
            elif n == 3:
                break
        
        os.system('cls')