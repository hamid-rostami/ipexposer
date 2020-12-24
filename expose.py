import asyncio
import asyncio_mqtt as mqtt
from asyncio_mqtt.error import MqttError
import aiohttp
import argparse
import platform
import re

# Default mqtt settings
MQTT_HOST = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_USER = ""
MQTT_PWD = ""
INTERVAL = 30
BASE_TOPIC = "ipexposer"

parser = argparse.ArgumentParser()
parser.add_argument("--host", dest="host", help="MQTT host")
parser.add_argument("--port", dest="port", help="MQTT post")
parser.add_argument("--user", dest="user", help="MQTT username")
parser.add_argument("--pwd", dest="pwd", help="MQTT password")
parser.add_argument("-i", dest="interval", type=int, help="Interval")

args = parser.parse_args()

mqtt_host = args.host or MQTT_HOST
mqtt_port = args.port or MQTT_PORT
mqtt_user = args.user or MQTT_USER
mqtt_pwd = args.pwd or MQTT_PWD
interval = args.interval or INTERVAL
hostname = platform.node()
topic = f"{BASE_TOPIC}/{hostname}"

print(f"Your hostname is: {hostname}")


async def mqtt_connect():
    while True:
        client = mqtt.Client(
            mqtt_host, port=mqtt_port, username=mqtt_user, password=mqtt_pwd
        )
        try:
            await client.connect()
            return client
        except MqttError:
            print("Connection error, retry in 5 sec")
            await asyncio.sleep(5)


async def get_ip():
    session = aiohttp.ClientSession()
    try:
        resp = await session.get("http://checkip.dyndns.org")
    except Exception as e:
        print(type(e))
        return
    body = await resp.text()
    r = re.search("Current IP Address: ([\d.]+)", body)
    await session.close()
    return r.groups()[0]


async def main():
    client = await mqtt_connect()
    while True:
        if not client:
            client = await mqtt_connect()
        try:
            msg = await get_ip()
            if msg:
                await client.publish(topic, msg, qos=1, retain=1)
            await asyncio.sleep(interval)
        except MqttError:
            print("pub err")
            client = None
    print("disconnecting")
    await client.disconnect()


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Goodbye!")
