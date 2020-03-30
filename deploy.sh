tar -zcvf ccxt-trader.tar.gz src/

scp -o StrictHostKeyChecking=no ccxt-trader.tar.gz root@159.65.75.241:/root/
scp -o StrictHostKeyChecking=no requirements.txt root@159.65.75.241:/root/

ssh -o StrictHostKeyChecking=no root@159.65.75.241 tar -xvzf ccxt-trader.tar.gz
ssh -o StrictHostKeyChecking=no root@159.65.75.241 'touch src/database.ini ; echo "
[postgresql]
user=doadmin
password=imt6kws2bm7ffay8
host=coin-do-user-7113675-0.db.ondigitalocean.com
port=25060
database=defaultdb
sslmode=require" > src/database.ini'

