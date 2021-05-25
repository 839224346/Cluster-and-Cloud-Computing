# Cluster-and-Cloud-Computing
## Project Overview

 The focus of this assignment is to	harvest	tweets from	across the cities of Australia on	the UniMelb
Research Cloud	and	undertake	a	variety	of	social	media	data	analytics scenarios	that	tell	interesting
stories	 of	 life	 in	 Australian cities	 and importantly	 how	 the	 Twitter	 data	 can	 be	 used	
alongside/compared	 with/augment the	 data	 available	 within	 the	AURIN	 platform to	 improve	 our	
knowledge	of	life	in	the	cities of	Australia.


## Private Key to Run Ansible Playbook
### YjlmN2E2NTlkMzIzZTRh


# CCC Group 34
Team Members:
Congran Li    - 1035899
Haoyu Man     - 
Peiyu Zhu     - 1126549
Yi Wang       - 860072
Yiyang Jin    - 966255


## Video links


### Frontend presentation


### PPT
https://docs.google.com/presentation/d/1PV_Ui_XYZrv7qMABt_pXkZIt7Gh6DANiCvhuGUy27Ig/edit?usp=sharing


## Project Structure

### FrontEnd 
1. React  -> Nginx reverse proxy port 80
2. Data visualization
3. Google Map
4. Echarts

### BackEnd
1. Flask(6100)
2. CouchDB related interface
3. Data query interface

### Crawler
1. Apply for the Twitter Developer API
2. Scheduled by Crontab (running for every 15 mins)

### Data Loader
1. Load pre-processed data into database

### Natural Language Processing
1. Model and metrics: TextBlob, Pickle, Yake
2. Run the script periodically (the same script as Crawler)

### Deployment Operation 
1. Ansible creates 4 hosts with one click
2. Docker runs 3 CouchDB instances
3. Ansible controls Docker-compose with services on each instances 

### Server Arrangement

Server1: 172.26.37.225
    
    CouchDB/ couchdb:2.3.0
    Frontend/
    Nginx/ nginx:lastest
    CAdvisor/


Server2: 172.26.38.110
    
    CouchDB/couchdb:2.3.0
    Backend/ lihuanz/my-backend:lastest
    Spider/ 
    CAdvisor/


Server3: 172.26.38.1
    
    CouchDB/couchdb:2.3.0
    Backend/
    NLP/
    CAdvisor/


Server4: 172.26.38.11

    MachineLearning/
    Grafana/ grafana/grafana:lastest
    InfluxDB/ influxdb:lastest
    cAdvisor/ google/cadvisor:lastest
