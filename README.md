How to run:

conda create -n airsystem python=3.10 -y
conda activate airsystem
pip install flask mysql-connector-python

brew services start mysql

mysql -u root -p
database='AirTicketReservationSystem'
CREATE DATABASE AirTicketReservationSystem;
USE AirTicketReservationSystem;
mysql -u root -p AirTicketReservationSystem < TestData.sql
exit;

export FLASK_APP=new_app.py

flask run
