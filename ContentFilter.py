import json
import re

class Filter:
    def __init__(self):
        with open('config.json') as f:
            f = json.load(f)
            self.filter_list = f['CONTENT-FILTER']
    
    def block(self, url):
        for ele in self.filter_list:
            if re.search(ele, url):
                return True
        
        return False
    
    def Add_url(self, url):
        for i in range(len(self.filter_list)):
            if self.filter_list[i] == url:
                return
        
        self.filter_list.append(url)

        with open('config.json') as f:
            new_config = json.load(f)
        
        new_config['CONTENT-FILTER'] = self.filter_list

        with open('config.json', 'w') as f:
            f.write(json.dumps(new_config))
    
    def remove_url(self, url):
        for i in range(len(self.filter_list)):
            if self.filter_list[i] == url:
                self.filter_list[i], self.filter_list[len(self.filter_list)-1] = self.filter_list[len(self.filter_list)-1], self.filter_list[i]
                self.filter_list.pop()

                with open('config.json') as f:
                    new_config = json.load(f)
                
                new_config['CONTENT-FILTER'] = self.filter_list

                with open('config.json', 'w') as f:
                    f.write(json.dumps(new_config))
                
                break
