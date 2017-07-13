This program aims at making an image upload system using flask.

    The app uses Jinja2 templating in order to create interactive script to html parsing. Templates are stored in the templates folder, 
while routes are in the routes folder. static files with js, css, images and html are automatically created.

    We first create a registration page where users select a username and password which is then hashed and checked for errors.
Among these errors include whether the username is taken, passwords match and are of minimum length.

    We use MySQL as a database. A python script is then created in a package dbconnect to maintain the MYSQL connection.
We create an instance of this connection so that usernames and passwords are stored locally on a MySQL database and connected using MySQLdb.

    Once the username and password is stored the user is now logged in and can log in through the log in page. They are now redirected to the
main upload page. Here they can upload files to a locally stored folder called images. 

    These files are then accessed in the gallery.html template to display.