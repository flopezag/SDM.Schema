#!/usr/bin/env python
# -*- encoding: utf-8 -*-
##
# Copyright 2024 FIWARE Foundation, e.V.
#
# This file is part of SDM SQL schema generator
#
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
##
from fastapi import FastAPI, Request, Response, status
from fastapi.logger import logger as fastapi_logger
from uvicorn import run
from datetime import datetime
from cli.command import __version__
from secure import (
    Server,
    ContentSecurityPolicy,
    StrictTransportSecurity,
    ReferrerPolicy,
    PermissionsPolicy,
    CacheControl,
    Secure,
)
from logging import getLogger
from pathlib import Path
from api.custom_logging import CustomizeLogger
from json import load, JSONDecodeError
from ssl import SSLContext, PROTOCOL_TLS_SERVER
from common.SDMDescriptionFile import SDMDescriptionFile

initial_uptime = datetime.now()
logger = getLogger(__name__)
sdm_description_file = SDMDescriptionFile()


def create_app() -> FastAPI:
    app = FastAPI(title="SDM JSON Schema Retrieval Based On Entity Types", debug=False)

    custom_logger = CustomizeLogger()
    customize_logger = custom_logger.get_logger()

    fastapi_logger.addHandler(customize_logger)
    app.logger = customize_logger

    return app


application = create_app()


@application.middleware("https")
async def set_secure_headers(request, call_next):
    response = await call_next(request)
    server = Server().set("Secure")

    csp = (
        ContentSecurityPolicy()
        .default_src("'none'")
        .base_uri("'self'")
        .connect_src("'self'" "api.spam.com")
        .frame_src("'none'")
        .img_src("'self'", "static.spam.com")
    )

    hsts = StrictTransportSecurity().include_subdomains().preload().max_age(2592000)

    referrer = ReferrerPolicy().no_referrer()

    permissions_value = PermissionsPolicy().geolocation("self", "'spam.com'").vibrate()

    cache_value = CacheControl().must_revalidate()

    secure_headers = Secure(
        server=server,
        csp=csp,
        hsts=hsts,
        referrer=referrer,
        permissions=permissions_value,
        cache=cache_value,
    )

    secure_headers.framework.fastapi(response)

    return response


@application.get("/version", status_code=status.HTTP_200_OK)
def getversion(request: Request):
    request.app.logger.info("GET /version - Request version information")

    data = {
        "doc": "...",
        "git_hash": "nogitversion",
        "version": __version__,
        "release_date": "no released",
        "uptime": get_uptime(),
    }

    return data


@application.post("/entity", status_code=status.HTTP_200_OK)
async def get_json_schema(request: Request, response: Response):
    request.app.logger.info(f'POST /entity - Obtaining SDM JSON Schema')

    try:
        req_info = await request.json()
    except JSONDecodeError:
        request.app.logger.error("Missing JSON payload")

        resp = {
            "message": "It is needed to provide a JSON object in the payload with the key 'type' "
                       "and the value of a valid Entity Type"
        }

        response.status_code = status.HTTP_400_BAD_REQUEST
        return resp

    try:
        entity_type = req_info["type"]

        request.app.logger.debug(f'Request obtain the JSON Schema of the Entity Type: "{entity_type}"')
        data = sdm_description_file.get_data(entity_name=entity_type)

        # data = [{'jsonSchema': x['jsonSchema']} for x in data]
        request.app.logger.info(f"JSON Schema obtained successfully: {data}")

        response.status_code = status.HTTP_200_OK
        return data

    except KeyError as e:
        message = f"Unexpected {e=}, {type(e)=}"
        request.app.logger.error(message)

        resp = {
            "message": message
        }

        response.status_code = status.HTTP_400_BAD_REQUEST
        return resp


def get_uptime():
    now = datetime.now()
    delta = now - initial_uptime

    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)

    fmt = "{d} days, {h} hours, {m} minutes, and {s} seconds"

    return fmt.format(d=days, h=hours, m=minutes, s=seconds)


def launch(app: str = "server:application", host: str = "127.0.0.1", port: int = 5700):
    ssl_context = SSLContext(PROTOCOL_TLS_SERVER)

    logging_config_path = Path.cwd().joinpath("common/config.json")
    with open(logging_config_path) as config_file:
        config = load(config_file)

    ssl_context.load_cert_chain(certfile=config["cert"], keyfile=config["key"])

    run(
        app=app,
        host=host,
        port=port,
        log_level="info",
        server_header=False,
        ssl_certfile=config["cert"],
        ssl_keyfile=config["key"]
    )


if __name__ == "__main__":
    launch()
