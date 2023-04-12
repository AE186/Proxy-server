from multiprocessing import Process
import os
import WebProxy

if __name__ == "__main__":
    proxy = WebProxy.WebProxy()

    process = Process(target=proxy.run)
    process.start()

    while True:
        print("1) Block URL")
        print("2) Remove Blocked URL")
        print("3) Exit\n")

        n = input("Option: ")

        if n.isnumeric():
            n = int(n)

            if n == 1:
                url = input("Enter URL: ")
                proxy.block(url)
            elif n == 2:
                url = input("Enter URL: ")
                proxy.unblock(url)
            elif n == 3:
                break
        
        os.system('cls')
    
    process.kill()