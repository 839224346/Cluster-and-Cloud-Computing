declare -a nodes=(172.26.133.10 172.26.129.163 172.26.131.108)
export masternode=`echo ${nodes} | cut -f1 -d' '`
export user='admin'
export pass='admin'
export VERSION='3.1.1'
export cookie='a192aeb9904e6590849337933b000c99'


docker stop $(docker ps --all --filter "name=couchdb${masternode}" --quiet) 
docker rm $(docker ps --all --filter "name=couchdb${masternode}" --quiet)



echo "== Start the containers =="
docker create\
      --net host\
      --name couchdb${masternode}\
      --env COUCHDB_USER=${user}\
      --env COUCHDB_PASSWORD=${pass}\
      --env COUCHDB_SECRET=${cookie}\
      --env ERL_FLAGS="-setcookie \"${cookie}\" -name \"couchdb@${masternode}\""\
      ibmcom/couchdb3:${VERSION}

declare -a conts=(`docker ps --all | grep couchdb | cut -f1 -d' ' | xargs -n${size} -d'\n'`)
for cont in "${conts[@]}"; do docker start ${cont}; done

docker exec couchdb${masternode} bash -c "echo \"-setcookie couchdb_cluster\" >> /opt/couchdb/etc/vm.args"
docker exec couchdb${masternode} bash -c "echo \"-name couchdb@${masternode}\" >> /opt/couchdb/etc/vm.args"
docker exec couchdb${masternode} bash -c "echo \"-kernel inet_dist_listen_min 9100\" >> /opt/couchdb/etc/vm.args"
docker exec couchdb${masternode} bash -c "echo \"-kernel inet_dist_listen_max 9200\" >> /opt/couchdb/etc/vm.args"

docker restart couchdb${masternode}
sleep 3
