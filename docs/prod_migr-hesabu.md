
# Allow the hesabu manager to talk to the new hesabu server

In the `System Settings > Access > CORS whitelist`

make sure to add https://hesabu.${DOMAIN_NAME}

![image](https://user-images.githubusercontent.com/371692/225247412-d56c91c5-9664-47b3-bd92-69217ce73315.png)


# Make the hesabu manager talk to the new hesabu server

Last step is to change the "hesabu" config through the dhis2 menu

`Datastore management > hesabu > hesabu `

There 
- edit the url field with `https://hesabu.${DOMAIN_NAME}` (no trailing slash) and
- change the `programId` (probably to 1 if you restored a production dump)

![image](https://user-images.githubusercontent.com/371692/225250012-97cb1a3d-b17f-4753-b4b6-47b0af6a80cb.png)

# Deploy the invoice app with a "recent" blsq-report-components

if the invoice app is on bitbucket and using our standard deployment script
adapt 

Override the repository variable `REACT_APP_ORBF2_URL` (the default value is inherited at workspace/organisation level) with the value `https://hesabu.${DOMAIN_NAME}` (adapt the domain name)

Then redeploy

Verify it takes effect (check and invoice, look in the network view you should see call to the new server)