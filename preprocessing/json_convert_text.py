import json
import os
import sys

file1 = 'final-final.json'


f1 = open(file1)


json1 = json.load(f1)





with open('final.txt', 'w') as fp:
    for i in range(len(json1)):
        for j in range(len(json1[i]["lga_areas"])):
            # print(json1[i]["lga_areas"][j]["properties"]['keyword_data'])
            new_dict = {}
            new_dict['starttime'] = json1[i]['id']
            new_dict['lga_id'] = json1[i]["lga_areas"][j]['lga_id']
            new_dict['properties'] = json1[i]["lga_areas"][j]["properties"]
            r = json.dumps(new_dict)
            fp.write(r)
            fp.write('\n')

