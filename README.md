# Interactify
 Social Media Website

# To download and install this application on Docker on Ubuntu Server run the following commands:

$ sudo git clone https://github.com/Ewsmyth/Interactify.git

$ cd Interactify

$ sudo docker build -t interactify-image .

$ sudo docker volume create interactify_data

$ sudo docker run -d -p 8585:8585 -v interactify_data:/var/lib/docker/volumes/interactify_data -v ~/Interactify:/Interactify interactify-image