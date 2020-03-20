tar -zcvf ccxt-trader.tar.gz src/

scp -o StrictHostKeyChecking=no ccxt-trader.tar.gz ec2-user@ec2-34-219-56-114.us-west-2.compute.amazonaws.com:/home/ec2-user
scp -o StrictHostKeyChecking=no requirements.txt ec2-user@ec2-34-219-56-114.us-west-2.compute.amazonaws.com:/home/ec2-user

ssh -o StrictHostKeyChecking=no ec2-user@ec2-34-219-56-114.us-west-2.compute.amazonaws.com tar -xvzf ccxt-trader.tar.gz
ssh -o StrictHostKeyChecking=no ec2-user@ec2-34-219-56-114.us-west-2.compute.amazonaws.com "cd src/ ; nohup python3.7 DataBaseDriver.py >/dev/null 2>&1 &"
