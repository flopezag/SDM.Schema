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
"""Python service to recover the SDM JSON Schema of a data models based on the Entity Type data


Usage:
  sdm_schema.py run (--entity_type ENTITY_TYPE)
  sdm_schema.py server [--host HOST] [--port PORT]
  sdm_schema.py (-H | --help)
  sdm_schema.py --version

Arguments:
  ENTITY_TYPE   Entity Type to look for the JSON Schema
  PORT          HTTP port used by the service

Options:
  -e, --entity_type <Entity Type>  Entity Type to obtain the corresponding JSON Schema
  -h, --host HOST                  Launch the server in the corresponding host
                                   [default: 127.0.0.1]
  -p, --port PORT                  Launch the server in the corresponding port
                                   [default: 5600]
  -H, --help                       Show this help message and exit
  -v, --version                    Show version and exit

"""

from docopt import docopt
from os.path import basename
from sys import argv
from schema import Schema, And, Or, Use, SchemaError  # type: ignore


__version__ = "0.1.0"
__author__ = "fla"


def parse_cli() -> dict:
    if len(argv) == 1:
        argv.append("-h")

    version = f"SDM JSON Schema request version {__version__}"

    args = docopt(__doc__.format(proc=basename(argv[0])), version=version)

    schema = Schema(
        {
            "--help": bool,
            "--entity_type": Or(
                None,
                str,
                error="--entity_type ENTITY_TYPE, Entity Type to obtain the corresponding JSON Schema"
            ),
            "--port": Or(
                None,
                And(Use(int), lambda n: 1 < n < 65535),
                error="--port N, N should be integer 1 < N < 65535"
            ),
            "--host": Or(
                None,
                str,
                error="--host HOST should be a string"
            ),
            "--version": bool,
            "run": bool,
            "server": bool,
        }
    )

    try:
        args = schema.validate(args)
    except SchemaError as e:
        exit(e)

    return args


if __name__ == "__main__":
    print(parse_cli())
