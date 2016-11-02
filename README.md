restart a beanstalk application, specificaly https://github.com/ucldc/potto-loris which
hangs in a specific way

```
usage: monitor.py [-h] [--detach] [--no-detach] [--pid PID] [--log LOG]
                  [--loglevel LOGLEVEL]
                  {start,stop,status,restart} ...

positional arguments:
  {start,stop,status,restart}

optional arguments:
  -h, --help            show this help message and exit
  --detach
  --no-detach
  --pid PID
  --log LOG
  --loglevel LOGLEVEL
```

crontab provided for restarting monitor deamon at reboot and as needed

`config.toml` needs to go in the same dir as `monitor.py`

```toml
[aws]
region = "us-west-2"

[iiif.prod]
application = "beanstalk-app"
environment = "beanstalk-prod-env"
url = "http://beanstalk-prod-en.us-west-2.elasticbeanstalk.com/"

[iiif.test]
application = "beanstalk-app"
environment = "beanstalk-test-env"
url = "http://beanstalk-test-env.us-west-2.elasticbeanstalk.com/"
```
