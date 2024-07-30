# SDM-Schema
The SDM-Schema is a Python service to recover the SDM JSON Schema of a data model based on the Entity Type data.

# Service usage guide

To run the code use the following commands and instructions:

```shell
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
                                  [default: 5700]
 -H, --help                       Show this help message and exit
 -v, --version                    Show version and exit
```


# OpenAPI documentation

the full OpenAPI specification is located under [doc/openapi.yaml](doc/openapi.yaml).

It provides an OpenAPI specification with two paths: `/version` and `/entity`.

## `/version` Endpoint:
- **GET Method**: Returns version information, including the documentation string, Git hash, version number, release date, and uptime.


## `/entity` Endpoint:
- **POST Method**: Designed to obtain the SDM JSON Schema based on the specified Entity Type.
- Request Body: The API receives a JSON object in the payload containing a required key, "type", with its value representing the corresponding Entity Type for which the JSON Schema is requested.
- Response: The API returns an array of dictionaries, each containing the key 'jsonSchema' with a value that is the link to the generated JSON Schema.


