# Using and running this template

This template uses quite a couple other programs that are used for differant parts of it.

The reconmended way to run this is via docker, however you can still run this without docker if you run each part seperatly

> Note: I except you to know how to use python and how to to edit the instructions to suite your environment.

# Setup
Before running this you must be running all other parts that are used in this:
- [Postgresql](#Postgresql)
- [KeyDB](#KeyDB)
- [Nats](#Nats)
- [Node.js](#Node.js)
- [Grafana](#Grafana)

## Postgresql
Postgresql is used as the primary database to store all infomation.

Install the latest postgresql and setup the database from the `schema.sql` file, make sure you edit the bot's config to point to your database with the corrent credentials.

## KeyDB

[KeyDB](https://keydb.dev/) is a multithreaded fork of redis, this is used for caching infomation that can be used by all the services in the bot.

We are Running keydb in LRU mode, you can change the max memory by editing the `keydb.conf`, you can also change the default password in here as well.

Install the latest keydb and run `keydb-server /path/to/this/repo/keydb.conf`.

Make sure you edit the bot's config to point to your keydb instance.

# Nats

[Nats](https://nats.io/) is used for IPC between all the parts of the bot.

Install the nats server and run `nats-server -p <enter port here>`.

Make sure to edit the bot's config to point to the nats server.

# Node.js
Node.js is a javascript runtime that is used to run the dashboard.

Install node.js
```bash
$ cd web
$ npm install -g yarn  # installs the yarn package manager
$ yarn i  # installs deps - might take a while and ignore the warnings
$ yarn dev/build/start  # dev runs it in dev mode, build creates a static build of it, start runs it
```

# Grafana

Grafana is a analitics dashboard that this bot uses.

Refer to https://grafana.com/docs/grafana/next/installation/ to see how to install grafana.

# Running
Make sure you did everything in the pre-setup beforehand

Edit the bots config file as much as you want.

```
$ python -m pip install -r requirements.txt
$ chmod +x ./launch
$ ./launch
```
