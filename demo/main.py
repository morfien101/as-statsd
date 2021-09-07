from as_statsd import statsd

import asyncio
import socket


datadog = statsd.Connector(
    host="127.0.0.1",
    port=8125,
    tag_type=statsd.Flavour.DATADOG,
    default_tags={"src_env": "local_dev"},
    ip_protocol=socket.IPPROTO_UDP,
)

telegraf = statsd.Connector(
    host="127.0.0.1",
    port=8125,
    tag_type=statsd.Flavour.TELEGRAF,
    default_tags={"src_env": "local_dev"},
    ip_protocol=socket.IPPROTO_UDP,
)


async def datadog_do_stuff() -> None:
    while True:
        for i in range(0, 100):
            print(i)
            datadog.incr("datadog", i, "1", tags={"tag1": "the dawg"})
            await asyncio.sleep(0.25)


async def telegraf_do_stuff() -> None:
    while True:
        for i in range(0, 100):
            print(i)
            telegraf.incr("telegraf", i, "1", tags={"tag1": "telegraf"})
            await asyncio.sleep(0.25)


async def main() -> None:
    await datadog.start()
    await telegraf.start()

    try:
        datadog_task = asyncio.create_task(datadog_do_stuff())
        telegraf_task = asyncio.create_task(telegraf_do_stuff())

        await asyncio.gather(telegraf_task, datadog_task)
    finally:
        await datadog.stop()
        await telegraf.stop()

asyncio.run(main())
