#!/bin/sh
sudo -s cp ./vtag.py /usr/local/bin/vtag
sudo -s chmod 755 /usr/local/bin/vtag

if [ -f /usr/local/bin/vtag ];
then
   echo "Successfully installed"
else
   echo "Failed to install"
fi