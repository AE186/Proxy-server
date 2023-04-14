import os
import ContentFilter

filter = ContentFilter.Filter()

while True:
        os.system('cls')
        print('Blocked urls:')
        for url in filter.get_block_list():
            print(f'\t{url}')

        print()
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
        