# AWS Lightsail Instance

## Create a Lightsail instance

```
ansible-playbook -e "instance_name=<instance_name> state=present" create-delete-instance.yml
```

## Delete a Lightsail instance

```
ansible-playbook -e "instance_name=<instance_name> state=absent" create-delete-instance.yml
```
