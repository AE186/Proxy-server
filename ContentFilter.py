import json
import re
import os

class Filter:
    def __init__(self) -> None:
        if not os.path.exists('filter.json'):
            filter_list = {'blocked-urls': []}
            with open('filter.json', 'w') as f:
                f.write(json.dumps(filter_list))

    def get_block_list(self):
        if os.path.exists('filter.json'):
            with open('filter.json') as f:
                f = json.load(f)
                return f['blocked-urls']
        
        return []
    
    def block(self, url):
        filter_list = self.get_block_list()

        for ele in filter_list:
            if re.search(ele, url):
                return True
        
        return False

    def Add_url(self, url):
        filter_list = self.get_block_list()

        for i in range(len(filter_list)):
            if filter_list[i] == url:
                return
        
        filter_list.append(url)

        with open('filter.json') as f:
            new_config = json.load(f)
        
        new_config['blocked-urls'] = filter_list

        with open('filter.json', 'w') as f:
            f.write(json.dumps(new_config))
    
    def remove_url(self, url):
        filter_list = self.get_block_list()

        for i in range(len(filter_list)):
            if filter_list[i] == url:
                filter_list[i], filter_list[len(filter_list)-1] = filter_list[len(filter_list)-1], filter_list[i]
                filter_list.pop()

                with open('filter.json') as f:
                    new_config = json.load(f)
                
                new_config['blocked-urls'] = filter_list

                with open('filter.json', 'w') as f:
                    f.write(json.dumps(new_config))
                
                break
