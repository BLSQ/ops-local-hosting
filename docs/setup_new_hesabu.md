# Setup Hesabu with empty data

- Connect to the hesabu container
```
sudo docker exec --detach-keys='ctrl-@'  -it  hesabu_hesabu-web_1 bash
```

- Create tables
```
bundle exec rake db:setup
```

- Create a program

Log in to hesabu interface with admin account to create a program

https://hesabu.<domain_name>/admin

Click on `Programs` in the list on the left, then click on `Add New`, fill in the `code` and `Save`.

- Create a user

Click on `Users` in the list on the left, then click on `Add New`, fill in the `Email` and `Password`, select the `Program` just created and `Save`.

Log out of admin account

- Create a project

Use this user's credentials to log into the hesabu interface and Click on `Projects` in the list on the left, then click on `Add New`, fill in the `name`, `dhis2 url`, `dhis2 user` and `dhis2 password`.


