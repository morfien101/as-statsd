Asynchronously send metrics to a statsd instance.

|build| |coverage| |sonar| |docs| |source| |download| |license|

This library provides connectors to send metrics to a statsd instance using either TCP or UDP.

.. code-block:: python

   import asyncio
   import time

   import as_statsd.statsd

   statsd = as_statsd.statsd.Connector(
      host=os.environ.get('STATSD_HOST', '127.0.0.1'))

   async def do_stuff():
      start = time.time()
      response = make_some_http_call()
      statsd.timing(f'timers.http.something.{response.code}',
                    (time.time() - start))

   async def main():
      await statsd.start()
      try:
         do_stuff()
      finally:
         await statsd.stop()

The ``Connector`` instance maintains a resilient connection to the target StatsD instance, formats the metric data
into payloads, and sends them to the StatsD target.  It defaults to using TCP as the transport but will use UDP if
the ``ip_protocol`` keyword is set to ``socket.IPPROTO_UDP``.  The ``Connector.start`` method starts a background
``asyncio.Task`` that is responsible for maintaining the connection.  The ``timing`` method enqueues a timing
metric to send and the task consumes the internal queue when it is connected.

The following convenience methods are available.  You can also call ``inject_metric`` for complete control over
the payload.

+--------------+--------------------------------------------------------------+
| ``incr``     | Increment a counter metric                                   |
+--------------+--------------------------------------------------------------+
| ``decr``     | Decrement a counter metric                                   |
+--------------+--------------------------------------------------------------+
| ``gauge``    | Adjust or set a gauge metric                                 |
+--------------+--------------------------------------------------------------+
| ``timer``    | Append a duration to a timer metric using a context manager  |
+--------------+--------------------------------------------------------------+
| ``timing``   | Append a duration to a timer metric                          |
+--------------+--------------------------------------------------------------+

If you are a `python-statsd`_ user, then the method names should look very familiar.  That is quite intentional.
I like the interface and many others do as well.  There is one very very important difference though -- the
``timing`` method takes the duration as the number of **seconds** as a ``float`` instead of the number of
milliseconds.

.. warning::

   If you are accustomed to using `python-statsd`_, be aware that the ``timing`` method expects the number of
   seconds as a ``float`` instead of the number of milliseconds.

.. _python-statsd: https://statsd.readthedocs.io/en/latest/

