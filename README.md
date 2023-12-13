# Interactify
 Social Media Website

# To download and install this application on Docker on Ubuntu Server run the following commands:

## You can run this command in any directory you want I just run it from the home directory
```
sudo git clone https://github.com/Ewsmyth/Interactify.git
```
## This should be altered to the proper path to the directory you cloned the git into
```
cd Interactify
```
## The period is for if you are inside the "Interactify" directory if you are not then you should replace this with the path to the Interactify directory
```
sudo docker build -t interactify-image .
```
## If you have already setup these volumes and you are just updating the app then you don't need to create the volumes again
```
sudo docker volume create interactify_data
```
## If you have already setup these volumes and you are just updating the app then you don't need to create the volumes again
```
sudo docker volume create interactify_userposts
```

```
sudo docker run -d -p 8585:8585 -v interactify_data:/var/lib/docker/volumes/interactify_data -v interactify_userposts:/var/lib/docker/volumes/interactify_userposts -v ~/Interactify:/Interactify interactify-image
```
