# [Watch Here!](https://youtu.be/BHJpKFnpUOA?si=ftnYeBkPqqVSxUYk)

# Setup
setup as in 

`requirement.txt` by  

    pip install -r requirements.txt

and follow steps in `README.txt`

# How to run

first, open terminal with `Ctl+Alt+t`

you need to loginto pepper with its IP, press its chest button and it will speak out the IP,

login with `ssh nao@ IP `

copy pepper_gpt/ in pepper (use choregraphe, it's easier)

open terminal, 

$ cd pepper_gpt/

$ unzip pepper_behaviors-f1daf1

$ mv pepper_behaviors-f1daf1 /home/nao/.local/share/PackageManager/apps/

$ cd

run python threaded.py


Second, open another terminal,

run `python module_receiver.py`

third, open another terminal again,

run `./march_gpt2.sh`


