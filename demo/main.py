from as_statsd import statsd
import time
import asyncio
import socket

sc = statsd.Connector(
    host="127.0.0.1",
    port="8125",
    tag_type="datadog",
    default_tags={"src_env": "local_dev"},
    ip_protocol=socket.IPPROTO_UDP
)


async def do_stuff():
    while True:
        for i in range(0, 100):
            print(i)
            sc.incr("tester", i, "1", tags={"tag1": "value1"})
            time.sleep(0.25)


async def main():
    await sc.start()
    try:
        do_stuff()
    finally:
        await statsd.stop()

asyncio.run(main())
