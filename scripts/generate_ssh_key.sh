read -P "Please specify email:" -e email
ssh-keygen -t rsa -b 4096 -C "$email"