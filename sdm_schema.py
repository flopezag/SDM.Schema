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

from cli.command import parse_cli
from api.server import launch
from common.SDMDescriptionFile import SDMDescriptionFile
from os.path import join, dirname
from logging import basicConfig, getLogger, DEBUG
from api.custom_logging import CustomizeLogger


def get_logger():
    custom_logger = CustomizeLogger()
    customize_logger = custom_logger.get_logger()

    return customize_logger


if __name__ == "__main__":
    logger = get_logger()
    args = parse_cli()

    if args["run"] is True:
        entity_type = args["--entity_type"]

        sdm_description = SDMDescriptionFile()

        try:
            response = sdm_description.get_links(entity_name='caca')
            print(response)
            sdm_description.stop()
        except IndexError as e:
            print(f'Unable to find the Entity Name: {entity_type}')
            logger.error(f'Unable to find the Entity Name: {entity_type}')
            sdm_description.stop()

    elif args["server"] is True:
        port = int(args["--port"])
        host = args["--host"]

        launch(app="api.server:application", host=host, port=port)
