<!-- # telegram_bot -->
-----------------------------------------
To run on FileZila:  screen -S telegram_bot
-----------------------------------------
pip3 install -r requirenments.txt
sudo apt-get install libpq-dev python-dev
pip3 install psycopg2
-----------------------------------------
To activate virtualenv:  source venv/bin/activate
-----------------------------------------
To start bot:  python3 mybot.py file.json
To start listen notify db:  python3 listen.py
-----------------------------------------
To use main.py to send users message:
  python3 main.py sendall Message
  python3 main.py send user1 user2 ... message
