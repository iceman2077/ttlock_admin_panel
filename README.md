# ttlock_admin_panel


## How to run the application

1) create an account at https://open.ttlock.com/reg
2) create an application. The application needs to be reviewed. After it is reviewed, all the APIs are available.
3) Create config.ini file that contain:
```bash
[ttlock_admin_panel]
client_id = 
client_secret = 
redirect_uri =
```
4) Use the package manager pip to install requered packages.
```bash
python -m pip install -r requrements.txt
```
5) Run following command to start flask
```bash
export FLASK_APP=ttlock_admin_panel
export FLASK_DEBUG=1
python -m flask run
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

