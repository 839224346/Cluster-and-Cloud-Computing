from datetime import datetime
import json
FILENUM=9    
with open('processed-9M.txt', 'r') as f:
    files = []
    for i in range(FILENUM):
        files += open('processed-9M-'+str(i)+'.txt', 'w'),

    count = 0
    for line in f:
        count += 1
        _dict = json.loads(line),
        index = count % FILENUM
        files[index].write(json.dumps(_dict))
        files[index].write('\n')
        