from as_statsd import statsd
import time
import asyncio
import socket

loop = asyncio.get_event_loop()

sc = statsd.Connector(
    host="127.0.0.1",
    port="8125",
    tag_type="datadog",
    default_tags={"src_env": "local_dev"},
    ip_protocol=socket.IPPROTO_UDP,
    loop=loop
)


async def do_stuff():
    while True:
        for i in range(0, 100):
            print(i)
            sc.incr("tester", i, "1", tags={"tag1": "value1"})
            await asyncio.sleep(0.25)


async def main():
    await sc.start()
    try:
        await do_stuff()
    finally:
        await sc.stop()

loop.run_until_complete(main())
