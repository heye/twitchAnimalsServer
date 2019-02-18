pkill -f python
cd /home/ubuntu/server
su - he -c "cd /home/he/schmatteoServer && git fetch"
su - he -c "cd /home/he/schmatteoServer && git reset --hard origin/master"
cd /home/he/schmatteoServer
nohup python3.5 -m server.main >/dev/null 2>&1 &
pgrep python