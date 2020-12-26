# What is this?

This is a simple hack to findout IP of your home server, if your
IP isn't static and changes over time. So you can run this script on your
server and retrive the IP whenever you want.

[Watch this asciinema](https://asciinema.org/a/381242)

# How to install?

Install requirements using pipenv

```bash
pipenv install
```

# How to use?

## On your server:

Run the script within the virtual environment

```
pipenv shell
python exposer.py
```

Use `-h` switch to see more options

## To lookup the ip:

```
mosquitto_sub -h test.mosquitto.org -t 'ipexposer/HOSTNAME'
```

Note: `HOSTNAME` is your hostname of your server

# Principle of working

After run the script, it tries to connect to a MQTT broker. by default
[Mosquitto](https://test.mosquitto.org)
free broker has been used, but you
can use any other MQTT broker. After connect to a broker, the script try
to retrive external ip of the server (the IP that is assigned
to your router). For this purpose, the script fetches
[this](http://checkip.dyndns.org)
URL to findout the IP. After that, the IP is published to a topic like
`ipexposer/HOSTNAME`, which hostname is hostname of your server.

To lookup the ip, you can simply use a MQTT client like `mosquitto_sub`.
Just subscribe to the topic and then you can see the IP. Please note that
if you're using mosquitto.org test broker, it may be a little slow because of its
heavy load. The interesting point is because the script set `retain` flag of
published message, you can see the latest IP even if the script is sopped
at the moment.
