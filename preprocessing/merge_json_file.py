import json
import os
import sys


file1 = 'c1.json'
file2 = 'b4.json'

f1 = open(file1)
f2 = open(file2)

json1 = json.load(f1)
json2 = json.load(f2)



for i in range(len(json1)):
    for j in range(len(json1[i]["lga_areas"])):
        # print(json1[i]["lga_areas"][j]["properties"])
        properties1 = json1[i]["lga_areas"][j]["properties"]
        properties2 = json2[i]["lga_areas"][j]["properties"]
        #normal values
        covid_attention1 = properties1['covid_attention']
        covid_attention2 = properties2['covid_attention']
        emotion_score1 = properties1['emotion_score']
        emotion_score2 = properties2['emotion_score']
        fin_tweet_num1 = properties1['fin_tweet_num']
        fin_tweet_num2 = properties2['fin_tweet_num']

        covid_attention3 = covid_attention1 + covid_attention2
        emotion_score3 = (emotion_score1 + emotion_score2) / 2
        fin_tweet_num3 = covid_attention1 + covid_attention2

        properties1['covid_attention'] = covid_attention3
        properties1['emotion_score'] = emotion_score3
        properties1['fin_tweet_num'] = fin_tweet_num3
        #keyword_data
        keyword_data1 = properties1['keyword_data']
        keyword_data2 = properties2['keyword_data']
        keyword_data3 = properties1['keyword_data'] + properties2['keyword_data']
        properties1['keyword_data'] = keyword_data3
        #emotion component
        emotion_component1 = properties1['emotion_component']
        emotion_component2 = properties2['emotion_component']
        emotion_component_positive1 = emotion_component1['positive']
        emotion_component_positive2 = emotion_component2['positive']
        emotion_component_neutral1 = emotion_component1['neutral']
        emotion_component_neutral2 = emotion_component2['neutral']
        emotion_component_negative1 = emotion_component1['negative']
        emotion_component_negative2 = emotion_component2['negative']

        emotion_component_positive3 = emotion_component_positive1 + emotion_component_positive2
        emotion_component_neutral3 = emotion_component_neutral1 = emotion_component_neutral2
        emotion_component_negative3 = emotion_component_negative1 + emotion_component_negative2

        properties1['emotion_component']['positive'] = emotion_component_positive3
        properties1['emotion_component']['neutral'] = emotion_component_neutral3
        properties1['emotion_component']['negative'] = emotion_component_negative3
        #children   
        children1 = properties1['children']['children']
        children2 = properties2['children']['children']
        properties1['children']['value'] = properties1['children']['value'] + properties2['children']['value']

        for k in range(len(children1)):
            for l in range(len(properties1['children']['children'][k]['children'])):
                # print(properties1['children']['children'][k]['children'][l])
                properties1['children']['children'][k]['children'][l]['value'] = properties1['children']['children'][k]['children'][l]['value'] + properties2['children']['children'][k]['children'][l]['value']

        json1[i]["lga_areas"][j]["properties"] = properties1


with open('final.json', 'w') as fp:
    json.dump(json1, fp)