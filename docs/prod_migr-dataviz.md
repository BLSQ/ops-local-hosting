
# Allow the dataviz manager to talk to the new dataviz backend server

In the `System Settings > Access > CORS whitelist`

make sure to add https://dataviz-backend.${DOMAIN_NAME}

![image](https://user-images.githubusercontent.com/371692/225247412-d56c91c5-9664-47b3-bd92-69217ce73315.png)



# Make the dataviz manager talk to new dataviz backend server


Make sure the most recent dataviz manager has been installed. 
It's the only one allowing to override the url for local hosting purpose. 

Last step is to change the "Dataviz Manager" config through the dhis2 menu

`Datastore management > blsq-dataviz > <<your-project>> `

there add an url field with `https://dataviz-backend.${DOMAIN_NAME}` (no trailing slash)

![image](https://user-images.githubusercontent.com/371692/225242514-b1ff3fd7-bf9a-4421-bd8f-fcf5f493d505.png)


(note if you redeploy the manager, you'll need to update it again)
