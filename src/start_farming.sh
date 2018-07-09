kill -9 $(pidof python farm) 
echo "Starting the process again"
source .secret
nohup python farm.py &
#./Web/start_site.sh
