tar -zcvf taapi-js.tar.gz taapi-js/

scp -o StrictHostKeyChecking=no taapi-js.tar.gz root@159.65.75.241:/root/

ssh -o StrictHostKeyChecking=no root@159.65.75.241 tar -xvzf taapi-js.tar.gz
ssh -o StrictHostKeyChecking=no root@159.65.75.241 'cd taapi-js && npm install && tmux && node index.js'