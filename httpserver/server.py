from aiohttp import web
import nats
import toml
import sys

from utils import verify_signature

config_name = sys.argv[1] if len(sys.argv) >= 2 else "configs/config.toml"

with open(config_name) as f:
    config = toml.load(f)

signing_key = config["stripe"]["signing_key"]

routes = web.RouteTableDef()

@routes.post('/stripe')
async def stripe_hook(request: web.Request):
    if not verify_signature(request, signing_key):
        return web.Response(status=401)

    print(await request.json())
    return web.Response()

async def connect_nats(app: web.Application):
    app["nats"] = await nats.connect(url=config["nats"]["url"])

async def close_nats(app: web.Application):
    await app["nats"].close()

app = web.Application()
app.on_startup.append(connect_nats)
app.add_routes(routes)
web.run_app(app, host="0.0.0.0", port=8080)
