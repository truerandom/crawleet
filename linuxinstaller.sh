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
echo "Installing crawleet"
echo "Please wait"
apt-get -qq update
status $? "apt update -y"
apt-get -qq install tor -y
status $? "tor install"
apt-get -qq install graphviz -y
status $? "graphviz install"
apt-get -qq install python-pip -y
status $? "python-pip install"
pip install requests -q
status $? "requests install"
pip install anytree -q
status $? "anytree install"
pip install lxml -q
status $? "lxml install"
mkdir -p /usr/bin/crawleet/
status $? "making dir /usr/bin/crawleet"
cp -r * /usr/bin/crawleet/
status $? "copying data to /usr/bin/crawleet"
ln -s /usr/bin/crawleet/crawleet.py /bin/crawleet
status $? "making link to /bin/crawleet"
chmod +x /bin/crawleet
status $? "applying permissions at /bin/crawleet"
echo "Installation finished"
echo "Use crawleet -h to see options"
