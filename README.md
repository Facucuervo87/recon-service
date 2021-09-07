# recon-service

This tool is to take subdomains from the security trails api key

To start the context of mongo db and django web server:

change the username and the projectname on ```views.py``` to take the right db and collection, then run docker-compose

```sudo docker-compose -f recon.yml up```

once mongo and docker was running, we could run the recon-securityTrails.py as following:

```python3 recon-securityTrails.py <Domain> <API-SecurityTrails> <projectname> <username>```


once the recon finish, you could see the results on ```http://localhost:8000/subdomains``` and downlad as csv file.
