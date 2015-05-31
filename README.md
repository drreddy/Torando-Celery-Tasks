Tornado Celery Queuing App
==

> This is just a test app implementing a queuing service using Celery (Using AMQP) and Python Tornado. In addition to the above tornado-celery was used to connect tornado and celery.

##### [App's Local Working Screenshot and Explanation](http://tornado-queue.herokuapp.com/)

##### Note: To run this app locally you need to have install amqp (messaging)

Local Installation & Running
--------------
```sh
git clone git@github.com:drreddy/Torando-Celery-Tasks.git
cd Torando-Celery-Tasks
pip install -r requirements.txt
celery -A tasks worker --loglevel=info
python server.py
```