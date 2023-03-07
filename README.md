# Kandilli observatory Earthquake Tracker 

This script calls the following resource and sends an email with AWS SES if there are more earthquakes than the threshold.

I developed this script because I was spending lots of time checking the earthquake data manually.


__Source:__  http://www.koeri.boun.edu.tr/scripts/lst5.asp

__python version__ >= 3.8

Before running this app you must __change the .env_example file name to .env and provide the required parameters__.


### Build Container & Run the app:

```shell
docker-compose build
docker-compose up -d
```


### Manually Run:

If you run it manually you must export the env variables to the console. Look at the follow-up example.
```shell
pip install -r requirements.txt
python main.py
```

### Environments:
```shell
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=
export AWS_REGION=eu-central-1
export PLACE="MARMARA DENIZI"
export THRESHOLD=8
export EMAIL_FROM=
export EMAIL_TO=
export EMAIL_SUBJECT="Number of earthquakes exceeded the threshold value"
```