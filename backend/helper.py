from datetime import datetime
from datetime import timezone
import couchdb
import conf
import copy
def get_months():

    years = []
    months = []
    day = 1

    for i in range(2020, 2022):
        years.append(i)

    for i in range(1,13):
        months.append(i)

    temp_each_month = []

    for year in years:
        for month in months:
            date = datetime(year, month, day).replace(tzinfo=timezone.utc)
            datestamp = date.timestamp()
            temp_each_month.append(str(int(datestamp)))

    month_periods = []
    for i in range(len(temp_each_month)-1):
        month_periods.append((temp_each_month[i], temp_each_month[i+1]))

    return temp_each_month


def get_scores_from_cached_data(starttime, endtime):
    couch = couchdb.Server('http://admin:admin@localhost:5984/')
    db = couch['final']
    mytemp = db.get('_design/example')
    if mytemp is not None:
        del db['_design/example']
    
    viewData = {
    "properties":{
        "map":"function(doc){ if (doc.starttime > "+ starttime +  " && doc.starttime <"+ endtime +") emit(doc._id, {properties: doc.properties, lga_ida: doc.lga_id});}",
        "reduce":"function (key, values) {  return values; }"
        }
    }
    score={}
    db['_design/example'] = dict(language='javascript', views=viewData)
    property_view = db.view('example/properties',group = True)

    # print(property_view)
    for row in property_view:
        continue
        print(row.value) 
    
    properties = {}

    json_format = {
        "tweet_num": 0,
        "emotion_score": 0,
        "keyword": [],
        "emotion_component": {
            "positive": 0,
            "neutral": 0,
            "negative": 0
        },
        "children": {
            'name': 'Whitehorse', 
            'value': 0, 
            'children': 
            [
                {
                    'name': 'positive',
                    'value': 0, 
                    'children': 
                    [
                        {
                            'name': 'subjective', 
                            'value': 0
                            }, 
                        {
                            'name': 'objective', 
                            'value': 0
                        }
                    ]
                },  
                {
                    'name': 'neutral', 
                    'value': 0, 
                    'children': 
                    [
                        {
                            'name': 'subjective', 
                            'value': 0
                        }, 
                        {
                            'name': 'objective', 
                            'value': 0
                        }
                    ]
                }, 
                {
                    'name': 'negative', 
                    'value': 0, 
                    'children': 
                    [
                        {
                            'name': 'subjective', 
                            'value': 0
                        }, 
                        {
                            'name': 'objective', 
                            'value': 0
                        }
                    ]
                }
            ]
        }
    }
    final_result = {}
    for i in conf.new_lga_id:
        test = copy.deepcopy(json_format)
        final_result[str(i)] = test
    count = 0
    for row in property_view:
        count += 1
        item = row.value

        lga_id = item[0][0]["lga_ida"]
        new_item = item[0][0]["properties"]
        final_result[str(lga_id)]['tweet_num'] += new_item["fin_tweet_num"]
        final_result[str(lga_id)]['emotion_score'] = (final_result[str(lga_id)]['emotion_score'] + new_item["emotion_score"]) / 2
        if len(new_item["keyword_data"]) != 0:
            final_result[str(lga_id)]['keyword'].append(new_item["keyword_data"][0])
        final_result[str(lga_id)]['emotion_component']['positive'] += new_item['emotion_component']['positive']
        final_result[str(lga_id)]['emotion_component']['neutral'] += new_item['emotion_component']['neutral']
        final_result[str(lga_id)]['emotion_component']['negative'] += new_item['emotion_component']['negative']
        final_result[str(lga_id)]['children']['value'] += new_item['children']['value']
        final_result[str(lga_id)]['children']['children'][0]['value'] += new_item['children']['children'][0]['value']
        final_result[str(lga_id)]['children']['children'][1]['value'] += new_item['children']['children'][1]['value']
        final_result[str(lga_id)]['children']['children'][2]['value'] += new_item['children']['children'][2]['value']
        final_result[str(lga_id)]['children']['children'][0]['children'][0]['value'] += new_item['children']['children'][0]['children'][0]['value']
        final_result[str(lga_id)]['children']['children'][0]['children'][1]['value'] += new_item['children']['children'][0]['children'][1]['value']
        final_result[str(lga_id)]['children']['children'][1]['children'][0]['value'] += new_item['children']['children'][1]['children'][0]['value']
        final_result[str(lga_id)]['children']['children'][1]['children'][1]['value'] += new_item['children']['children'][1]['children'][1]['value']
        final_result[str(lga_id)]['children']['children'][2]['children'][0]['value'] += new_item['children']['children'][2]['children'][0]['value']
        final_result[str(lga_id)]['children']['children'][2]['children'][1]['value'] += new_item['children']['children'][2]['children'][1]['value']

#     print(final_result)
    return final_result


starttime = "1588291200"
endtime = "1690969600"

get_scores_from_cached_data(starttime, endtime)
