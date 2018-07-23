status(){
	bar="***********************************************"
	if [ "$1" -ne 0 ];then
		printf "$bar\nProblem $2\n$bar"
	fi
}
if [ "$(id -u)" != "0" ]; then
	echo "This script needs root"
	exit 1
fi
apt-get update
status $? "apt update -y"
apt-get install tor -y
status $? "tor install"
apt-get install graphviz -y
status $? "graphviz install"
apt-get install python-pip -y
status $? "python-pip install"
pip install requests
status $? "requests install"
pip install anytree
status $? "anytree install"
pip install lxml
status $? "lxml install"
mkdir -p /usr/bin/crawleet/
status $? "making dir /usr/bin/crawleet"
cp -r * /usr/bin/crawleet/
status $? "copying data to /usr/bin/crawleet"
ln -s /usr/bin/crawleet/crawleet.py /bin/crawleet
status $? "making link to /bin/crawleet"
chmod +x /bin/crawleet
status $? "applying permissions at /bin/crawleet"
