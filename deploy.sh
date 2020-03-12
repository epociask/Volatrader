tar -zcvf ccxt-trader.tar.gz src/

scp ccxt-trader.tar.gz ec2-user@ec2-34-219-56-114.us-west-2.compute.amazonaws.com:/home/ec2-user
scp requirements.txt ec2-user@ec2-34-219-56-114.us-west-2.compute.amazonaws.com:/home/ec2-user

ssh ec2-user@ec2-34-219-56-114.us-west-2.compute.amazonaws.com tar -xvzf ccxt-trader.tar.gz
