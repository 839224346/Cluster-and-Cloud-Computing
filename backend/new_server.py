import couchdb
import requests
import copy
import flask,json
from flask import request
from collections import Counter
from flask_cors import CORS

server = flask.Flask(__name__)
CORS(server, resources=r'/*')
# CORS(server, supports_credentials=True)

@server.route('/api/statistics/zone/melbourn',methods=['get'])
def statistics():  
    
    get_data = request.args.to_dict()
    # begintime = get_data.get('begintime')
    # endtime = get_data.get('endtime')

    # starttime = begintime
    # endtime = endtime

    file1=open('api_1.json')
    api1=json.load(file1)

    new_lga_id_34 = [20660, 20910, 21110,21180,21450,21610,21890,22170,22310,22670,23110,23270,23670,24130,24210,24330,24410,24600,24650,24850,24970,25060,25150,25250,25340,25620,25710,25900,26350,26980,27070,27260,27350,27450]
    lgaid_i_map_79 = {"20110": 0, "20260": 1, "20570": 2, "20660": 3, "20740": 4, "20830": 5, "20910": 6, "21010": 7, "21110": 8, "21180": 9, "21270": 10, "21370": 11, "21450": 12, "21610": 13, "21670": 14, "21750": 15, "21830": 16, "21890": 17, "22110": 18, "22170": 19, "22250": 20, "22310": 21, "22410": 22, "22490": 23, "22620": 24, "22670": 25, "22750": 26, "22830": 27, "22910": 28, "22980": 29, "23110": 30, "23190": 31, "23270": 32, "23350": 33, "23430": 34, "23670": 35, "23810": 36, "23940": 37, "24130": 38, "24210": 39, "24250": 40, "24330": 41, "24410": 42, "24600": 43, "24650": 44, "24780": 45, "24850": 46, "24900": 47, "24970": 48, "25060": 49, "25150": 50, "25250": 51, "25340": 52, "25430": 53, "25490": 54, "25620": 55, "25710": 56, "25810": 57, "25900": 58, "25990": 59, "26080": 60, "26170": 61, "26260": 62, "26350": 63, "26430": 64, "26490": 65, "26610": 66, "26670": 67, "26700": 68, "26730": 69, "26810": 70, "26890": 71, "26980": 72, "27070": 73, "27170": 74, "27260": 75, "27350": 76, "27450": 77, "27630": 78}

    try:
        couch = couchdb.Server('http://admin:admin@127.0.0.1:5984/')
        db = couch['ccc_re']
    except ConnectionRefusedError:
        err = {}
        err["name"] = "ConnectionRefusedError"
        err["message"] = "Database connection error."
        return json.dumps(err, ensure_ascii=False)
    else:
        mytemp = db.get('_design/example')
        if mytemp is not None:
            del db['_design/example']

    
        viewData = {
        "re":{
            "map":"function(doc){  emit(doc);}",
        }
        }
        db['_design/example'] = dict(language='javascript', views=viewData)

        re_view = db.view('example/re')
        for row in re_view:
            tweet_num_arr = row.key["tweet_num"]
            major_emotion = row.key["major_emotion"]
            emotion_component = row.key["emotion_component"]

        fin_covid_attention = tweet_num_arr
        fin_major_emotion = major_emotion
        fin_emotion_component = emotion_component

        for i in range(len(api1["features"])):
            api1["features"][i]["properties"]["covid_attention"] = fin_covid_attention[lgaid_i_map_79[str(new_lga_id_34[i])]]
            api1["features"][i]["properties"]["major_emotion"] = fin_major_emotion[lgaid_i_map_79[str(new_lga_id_34[i])]]
            api1["features"][i]["properties"]["emotion_component"] = fin_emotion_component[lgaid_i_map_79[str(new_lga_id_34[i])]]
            api1["features"][i]["properties"]["key_words"] = {}

        return json.dumps(api1, ensure_ascii=False)




@server.route('/api/statistics/relationship',methods = ['post'])
def queryRelationship():

    da=json.loads(request.data)


    # begintime = da.get('begintime')
    # endtime = da.get('endtime')
    query_lga = da.get('lga_id')
    

    # starttime = begintime
    # endtime = endtime

    # query_lga=[20660,22170]

    file2=open('api_2.json')
    api2=json.load(file2)


    try:
        couch = couchdb.Server('http://admin:admin@127.0.0.1:5984/')
        db = couch['ccc_re']
    except ConnectionRefusedError:
        err = {}
        err["name"] = "ConnectionRefusedError"
        err["message"] = "Database connection error."
        return json.dumps(err, ensure_ascii=False)
    else:
        mytemp = db.get('_design/example')
        if mytemp is not None:
            del db['_design/example']
    
        viewData = {
        "re":{
            "map":"function(doc){  emit(doc);}",
        }
        }
        db['_design/example'] = dict(language='javascript', views=viewData)

        re_view = db.view('example/re')

        for row in re_view:
            tweet_num_arr = row.key["tweet_num"]  
            emotion_score = row.key["emotion_score"]
        
        api2_tnum = tweet_num_arr   
        api2_emotion = emotion_score


        lgaid_i_map = {"20660": 0, "20910": 1, "21110": 2, "21180": 3, "21450": 4, "21610": 5, "21890": 6, "22170": 7, "22310": 8, "22670": 9, "23110": 10, "23270": 11, "23670": 12, "24130": 13, "24210": 14, "24330": 15, "24410": 16, "24600": 17, "24650": 18, "24850": 19, "24970": 20, "25060": 21, "25150": 22, "25250": 23, "25340": 24, "25620": 25, "25710": 26, "25900": 27, "26350": 28, "26980": 29, "27070": 30, "27260": 31, "27350": 32, "27450": 33}
        lgaid_i_map_79 = {"20110": 0, "20260": 1, "20570": 2, "20660": 3, "20740": 4, "20830": 5, "20910": 6, "21010": 7, "21110": 8, "21180": 9, "21270": 10, "21370": 11, "21450": 12, "21610": 13, "21670": 14, "21750": 15, "21830": 16, "21890": 17, "22110": 18, "22170": 19, "22250": 20, "22310": 21, "22410": 22, "22490": 23, "22620": 24, "22670": 25, "22750": 26, "22830": 27, "22910": 28, "22980": 29, "23110": 30, "23190": 31, "23270": 32, "23350": 33, "23430": 34, "23670": 35, "23810": 36, "23940": 37, "24130": 38, "24210": 39, "24250": 40, "24330": 41, "24410": 42, "24600": 43, "24650": 44, "24780": 45, "24850": 46, "24900": 47, "24970": 48, "25060": 49, "25150": 50, "25250": 51, "25340": 52, "25430": 53, "25490": 54, "25620": 55, "25710": 56, "25810": 57, "25900": 58, "25990": 59, "26080": 60, "26170": 61, "26260": 62, "26350": 63, "26430": 64, "26490": 65, "26610": 66, "26670": 67, "26700": 68, "26730": 69, "26810": 70, "26890": 71, "26980": 72, "27070": 73, "27170": 74, "27260": 75, "27350": 76, "27450": 77, "27630": 78}

        fin_lga_name = []
        fin_emotion_score = []
        fin_tweet_num = []
        fin_GP_num = []
        fin_education_rank = []
        fin_population_num = []
        fin_averge_income = []
        fin_averge_age = []
        fin_homeless_rate = []

        for each in query_lga:
            index = lgaid_i_map[str(each)]
            index2 = lgaid_i_map_79[str(each)]
    
            fin_lga_name.append(api2["data"]["lga_name"][index])
            fin_emotion_score.append(api2_emotion[index2])
            fin_tweet_num.append(api2_tnum[index2])
            fin_GP_num.append(api2["data"]["factor"]["GP_num"][index])
            fin_education_rank.append(api2["data"]["factor"]["education_rank"][index])
            fin_population_num.append(api2["data"]["factor"]["population_num"][index])
            fin_averge_income.append(api2["data"]["factor"]["averge_income"][index])
            fin_averge_age.append(api2["data"]["factor"]["averge_age"][index])
            fin_homeless_rate.append(api2["data"]["factor"]["homeless_rate"][index])
    
        api2["data"]["lga_name"] = fin_lga_name
        api2["data"]["factor"]["tweet_num"] = fin_tweet_num
        api2["data"]["factor"]["emotion_score"] = fin_emotion_score
        api2["data"]["factor"]["GP_num"] = fin_GP_num
        api2["data"]["factor"]["education_rank"] = fin_education_rank
        api2["data"]["factor"]["population_num"] = fin_population_num
        api2["data"]["factor"]["averge_income"] = fin_averge_income
        api2["data"]["factor"]["averge_age"] = fin_averge_age
        api2["data"]["factor"]["homeless_rate"] = fin_homeless_rate

        return json.dumps(api2, ensure_ascii=False)



@server.route('/api/statistics/lgaEmotion',methods = ['post'])
def querylgaEmotion():

    da=json.loads(request.data)

    # begintime = da.get('begintime')
    # endtime = da.get('endtime')
    query_lga = da.get('lga_id')

    # starttime = begintime
    # endtime = endtime

    try:
        couch = couchdb.Server('http://admin:admin@127.0.0.1:5984/')
        db = couch['ccc_re']
    except ConnectionRefusedError:
        err = {}
        err["name"] = "ConnectionRefusedError"
        err["message"] = "Database connection error."
        return json.dumps(err, ensure_ascii=False)
    else:

        mytemp = db.get('_design/example')
        if mytemp is not None:
          del db['_design/example']
    
        viewData = {
        "re":{
            "map":"function(doc){  emit(doc);}",
            }
        }
        db['_design/example'] = dict(language='javascript', views=viewData)

        re_view = db.view('example/re')

        new_lga_id_34 = [20660, 20910, 21110,21180,21450,21610,21890,22170,22310,22670,23110,23270,23670,24130,24210,24330,24410,24600,24650,24850,24970,25060,25150,25250,25340,25620,25710,25900,26350,26980,27070,27260,27350,27450]
        lgaid_i_map_79 = {"20110": 0, "20260": 1, "20570": 2, "20660": 3, "20740": 4, "20830": 5, "20910": 6, "21010": 7, "21110": 8, "21180": 9, "21270": 10, "21370": 11, "21450": 12, "21610": 13, "21670": 14, "21750": 15, "21830": 16, "21890": 17, "22110": 18, "22170": 19, "22250": 20, "22310": 21, "22410": 22, "22490": 23, "22620": 24, "22670": 25, "22750": 26, "22830": 27, "22910": 28, "22980": 29, "23110": 30, "23190": 31, "23270": 32, "23350": 33, "23430": 34, "23670": 35, "23810": 36, "23940": 37, "24130": 38, "24210": 39, "24250": 40, "24330": 41, "24410": 42, "24600": 43, "24650": 44, "24780": 45, "24850": 46, "24900": 47, "24970": 48, "25060": 49, "25150": 50, "25250": 51, "25340": 52, "25430": 53, "25490": 54, "25620": 55, "25710": 56, "25810": 57, "25900": 58, "25990": 59, "26080": 60, "26170": 61, "26260": 62, "26350": 63, "26430": 64, "26490": 65, "26610": 66, "26670": 67, "26700": 68, "26730": 69, "26810": 70, "26890": 71, "26980": 72, "27070": 73, "27170": 74, "27260": 75, "27350": 76, "27450": 77, "27630": 78}
        lgaid_i_map_34 = {"20660": 0, "20910": 1, "21110": 2, "21180": 3, "21450": 4, "21610": 5, "21890": 6, "22170": 7, "22310": 8, "22670": 9, "23110": 10, "23270": 11, "23670": 12, "24130": 13, "24210": 14, "24330": 15, "24410": 16, "24600": 17, "24650": 18, "24850": 19, "24970": 20, "25060": 21, "25150": 22, "25250": 23, "25340": 24, "25620": 25, "25710": 26, "25900": 27, "26350": 28, "26980": 29, "27070": 30, "27260": 31, "27350": 32, "27450": 33}
        new_lga_name_34 = ['Banyule', 'Bayside','Boroondara','Brimbank','Cardinia','Casey','Darebin','Frankston','Glen Eira','Greater Dandenong','Hobsons Bay','Hume','Knox','Macedon Ranges','Manningham','Maribyrnong','Maroondah','Melbourne','Melton','Mitchell','Monash','Moonee Valley','Moorabool','Moreland','Mornington Peninsula','Murrindindi','Nillumbik','Port Phillip','Stonnington','Whitehorse','Whittlesea','Wyndham','Yarra','Yarra Ranges']

        for row in re_view:
            possub_result = row.key["possub_result"]
            posobj_result = row.key["posobj_result"]
            neusub_result = row.key["neusub_result"]
            neuobj_result = row.key["neuobj_result"]
            negsub_result = row.key["negsub_result"]
            negobj_result = row.key["negobj_result"]

        fin_possub_result = possub_result
        fin_posobj_result = posobj_result
        fin_neusub_result = neusub_result
        fin_neuobj_result = neuobj_result
        fin_negsub_result = negsub_result
        fin_negobj_result = negobj_result

        for i in range(len(new_lga_id_34)):
            fin_possub_result.append(possub_result[lgaid_i_map_79[str(new_lga_id_34[i])]])
            fin_posobj_result.append(posobj_result[lgaid_i_map_79[str(new_lga_id_34[i])]])
            fin_neusub_result.append(neusub_result[lgaid_i_map_79[str(new_lga_id_34[i])]])
            fin_neuobj_result.append(neuobj_result[lgaid_i_map_79[str(new_lga_id_34[i])]])
            fin_negsub_result.append(negsub_result[lgaid_i_map_79[str(new_lga_id_34[i])]])
            fin_negobj_result.append(negobj_result[lgaid_i_map_79[str(new_lga_id_34[i])]])
        
        

        anlgajson = {
            "name":"null",
            "value":0,
            "children":[
                {
                    "name":"positive",
                    "value":0,
                    "children":[
                        {
                            "name":"subjective",
                            "value":0
                        },
                        {
                            "name":"objective",
                            "value":0
                        }
                    ]
                },
                {
                    "name":"neutral",
                    "value":0,
                    "children":[
                        {
                            "name":"subjective",
                            "value":0
                        },
                        {
                            "name":"objective",
                            "value":0
                        }
                    ]
                },
                {
                    "name":"negative",
                    "value":0,
                    "children":[
                        {
                            "name":"subjective",
                            "value":0
                        },
                        {
                            "name":"objective",
                            "value":0
                        }
                    ]
                }
            ]
        }

        api3 = {
            "data":[
                {
                    "name":"melb",
                    "children":[]
                }
            ]
        }

        lga_value_list = []

        for lga in query_lga:
    
            index = lgaid_i_map_34[str(lga)]    
            newlgajson = copy.deepcopy(anlgajson)
    
            newlgajson["children"][0]["value"] = fin_possub_result[index] + fin_posobj_result[index]
            newlgajson["children"][0]["children"][0]["value"] = fin_possub_result[index]
            newlgajson["children"][0]["children"][1]["value"] = fin_posobj_result[index]
            newlgajson["children"][1]["value"] = fin_neusub_result[index] + fin_neuobj_result[index]
            newlgajson["children"][1]["children"][0]["value"] = fin_neusub_result[index]
            newlgajson["children"][1]["children"][1]["value"] = fin_neuobj_result[index]
            newlgajson["children"][2]["value"] = fin_negsub_result[index] + fin_negobj_result[index]
            newlgajson["children"][2]["children"][0]["value"] = fin_negsub_result[index]
            newlgajson["children"][2]["children"][1]["value"] = fin_negobj_result[index]
            newlgajson["value"] = newlgajson["children"][0]["value"] + newlgajson["children"][1]["value"] + newlgajson["children"][2]["value"]
            newlgajson["name"] = new_lga_name_34[index]
            data = copy.deepcopy(newlgajson)
            lga_value_list.append(data)
        api3["data"][0]["children"] = lga_value_list

        return json.dumps(api3, ensure_ascii=False)

@server.errorhandler(400)
def bad_request(e):
    err = {}
    err["name"] = "400"
    err["message"] = "Unauthorized."
    return json.dumps(err, ensure_ascii=False)

@server.errorhandler(403)
def forbidden(e):
    err = {}
    err["name"] = "403"
    err["message"] = "Forbidden."
    return json.dumps(err, ensure_ascii=False)

@server.errorhandler(404)
def handle_404_error(e):
    err = {}
    err["name"] = "404 Not Found"
    err["message"] = "The requested URL was not found on the server."
    return json.dumps(err, ensure_ascii=False)

@server.errorhandler(405)
def method_not_allowed(e):
    err = {}
    err["name"] = "405"
    err["message"] = "Illegalmethod."
    return json.dumps(err, ensure_ascii=False)

@server.errorhandler(500)
def internal_server_error(e):
    err = {}
    err["name"] = "500"
    err["message"] = "An internal server error occurred."
    return json.dumps(err, ensure_ascii=False)
    

server.run(port = 6100,debug = True,host = '0.0.0.0',threaded = True)