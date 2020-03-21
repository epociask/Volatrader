tar -zcvf ccxt-trader.tar.gz src/

scp -o StrictHostKeyChecking=no ccxt-trader.tar.gz ec2-user@ec2-34-219-56-114.us-west-2.compute.amazonaws.com:/home/ec2-user
scp -o StrictHostKeyChecking=no requirements.txt ec2-user@ec2-34-219-56-114.us-west-2.compute.amazonaws.com:/home/ec2-user

ssh -o StrictHostKeyChecking=no ec2-user@ec2-34-219-56-114.us-west-2.compute.amazonaws.com tar -xvzf ccxt-trader.tar.gz
ssh -o StrictHostKeyChecking=no ec2-user@ec2-34-219-56-114.us-west-2.compute.amazonaws.com 'touch src/database.ini ; echo "
[postgresql]
user=doadmin
password=imt6kws2bm7ffay8
host=coin-do-user-7113675-0.db.ondigitalocean.com
port=25060
database=defaultdb
sslmode=require" > src/database.ini'

ssh -o StrictHostKeyChecking=no ec2-user@ec2-34-219-56-114.us-west-2.compute.amazonaws.com "cd src/ ; nohup python3.8 DataBaseDriver.py >/dev/null 2>&1 &"
