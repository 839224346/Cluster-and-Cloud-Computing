import json
import os
import sys

file1 = 'final.json'


f1 = open(file1)


json1 = json.load(f1)

for i in range(len(json1)):
    for j in range(len(json1[i]["lga_areas"])):
        # print(json1[i]["lga_areas"][j]["properties"]['keyword_data'])
        new_dict = {}
        for key_value_pair in json1[i]["lga_areas"][j]["properties"]['keyword_data']:
            new_dict[list(key_value_pair.keys())[0]] = key_value_pair[list(key_value_pair.keys())[0]]
        # print(new_dict)
        sorted_dict = {k: v for k, v in sorted(new_dict.items(), key=lambda item: item[1], reverse=True)}
        new_list = []
        count = 0
        for key in sorted_dict.keys():
            new_list.append(key)
            count += 1

            if count > 5 and sorted_dict[key] < 5: break
        print(new_list)
        json1[i]["lga_areas"][j]["properties"]['keyword_data'] = new_list


with open('final-final.json', 'w') as fp:
    json.dump(json1, fp)