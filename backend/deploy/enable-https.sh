#!/bin/sh
sudo cp job-server-https.service /etc/systemd/system/job-server.service
sudo systemctl enable job-server
sudo systemctl start job-server
systemctl status job-server
