# Cluster-and-Cloud-Computing
## Project Overview

 The focus of this assignment is to	harvest	tweets from	across the cities of Australia on	the UniMelb
Research Cloud	and	undertake	a	variety	of	social	media	data	analytics scenarios	that	tell	interesting
stories	 of	 life	 in	 Australian cities	 and importantly	 how	 the	 Twitter	 data	 can	 be	 used	
alongside/compared	 with/augment the	 data	 available	 within	 the	AURIN	 platform to	 improve	 our	
knowledge	of	life	in	the	cities of	Australia.





# CCC Group 34
Team Members:
Congran Li    - 1035899
Haoyu Man     - 893862
Peiyu Zhu     - 1126549
Yi Wang       - 860072
Yiyang Jin    - 966255


## Video links
https://youtu.be/3_aXRwZOCpQ

### Frontend presentation
https://youtu.be/3_aXRwZOCpQ

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
2. Ansible sets server envrionments 
3. Ansible deploys Front-end, Back-end, Couchdb cluster in Docker and initiates servers of Nginx, Crawler and Data Loader

### Server Arrangement

Server1: 172.26.132.20
    
    Frontend/ react
    Nginx/ 1.reverse proxy server 2.load balancer for backend


Server2: 172.26.133.10
    
    CouchDB/ master node
    Backend/ flask


Server3: 172.26.131.108
    
    CouchDB/ slave node 1
    Backend/ flask
    Data Loader/


Server4: 172.26.129.163
    
    CouchDB/ slave node 2
    Backend/ flask
    Crawler/ 
    
    
# Private Key to Run Ansible Playbook
## YjlmN2E2NTlkMzIzZTRh
