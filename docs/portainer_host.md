
# Create a container via portainer

 * Name : debug-host
 * Image : busybox:latest
 * In command & logging :
   - check interactive and tty
 * In volumes
    - click on bind
    - container : `/host`
    - host: `/

 ![image](https://github.com/BLSQ/ops-local-hosting/assets/371692/950b68c3-0b91-470f-984b-ae7bc8bde27c)

  * Runtime & Resources
    - specify : Privileged mode
   
![image](https://github.com/BLSQ/ops-local-hosting/assets/371692/9271b07f-1fce-4f89-b423-4b0813c363ca)


# Once in the console

chroot

```
chroot /host
```

# Now you can access the filesytem or reboot things

becareful ;)

