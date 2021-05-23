export node=172.26.129.163
export user='admin'
export pass='admin'
export VERSION='3.1.1'
export cookie='a192aeb9904e6590849337933b000c99'

docker stop $(docker ps --all --filter "name=couchdb${node}" --quiet) 
docker rm $(docker ps --all --filter "name=couchdb${node}" --quiet)

echo "== Start the containers =="
docker create\
      --net host\
      --name couchdb${node}\
      --env COUCHDB_USER=${user}\
      --env COUCHDB_PASSWORD=${pass}\
      --env COUCHDB_SECRET=${cookie}\
      --env ERL_FLAGS="-setcookie \"${cookie}\" -name \"couchdb@${node}\""\
      ibmcom/couchdb3:${VERSION}

declare -a conts=(`docker ps --all | grep couchdb | cut -f1 -d' ' | xargs -n${size} -d'\n'`)
for cont in "${conts[@]}"; do docker start ${cont}; done

docker exec couchdb${node} bash -c "echo \"-setcookie couchdb_cluster\" >> /opt/couchdb/etc/vm.args"
docker exec couchdb${node} bash -c "echo \"-name couchdb@${node}\" >> /opt/couchdb/etc/vm.args"
docker exec couchdb${node} bash -c "echo \"-kernel inet_dist_listen_min 9100\" >> /opt/couchdb/etc/vm.args"
docker exec couchdb${node} bash -c "echo \"-kernel inet_dist_listen_max 9200\" >> /opt/couchdb/etc/vm.args"

docker restart couchdb${node}
sleep 3