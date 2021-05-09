# Generic Bot

A bot template with basic stuff implemented, this uses postgresql and keydb (a redis fork with multithreading) for storage and caching.

> This uses cutting edge version of libs - use at your own risk of code breaking

# Running
- setup keydb and postgresql
- rename `config.example.toml` to `config.toml` and put it inside `configs/`
- edit values as nessesary
- install deps from `requirements.txt`
- `python bot.py`
- ???
- profit


## TODO
- [ ] clusters (k3s/k8s/nomad/diy)
- [ ] public dashboard for configs
- [ ] owner dashboard
    - [ ] grafana
    - [ ] prometheus

- [ ] payment systems
    - [ ] stripe
    - [ ] paypal
    - [ ] patreon

- [ ] message broker for dashboard <-> bot
- [ ] proper launcher (ties in with clusters)
- [ ] error handling
- [ ] sentry/logstash
- [ ] seemless scaling with clusters

- [ ] paginator
- [ ] menus
- [ ] comments around the code
- [ ] better instructions on usage

- [ ] 20 ft rope
- [ ] towel
