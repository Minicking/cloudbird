if [ ${PWD##*/} != "Server" ]
then
    echo "please run in root directory"
    exit
fi
python3 -m venv env
source env/bin/activate
env/bin/pip3 install -r requirements.txt
