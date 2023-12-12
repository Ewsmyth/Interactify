# Interactify
 Social Media Website

# To download and install this application on Docker on Ubuntu Server run the following commands:

# $ sudo git clone https://github.com/Ewsmyth/Interactify.git
#   You can run this command in any directory you want I just run it from the home directory

# $ cd Interactify
#   This should be altered to the proper path to the directory you cloned the git into

# $ sudo docker build -t interactify-image .
#   The period is for if you are inside the "Interactify" directory if you are not then you should replace this with the path to the Interactify directory

# $ sudo docker volume create interactify_data

# $ sudo docker run -d -p 8585:8585 -v interactify_data:/var/lib/docker/volumes/interactify_data -v ~/Interactify:/Interactify interactify-image