# PLATOON_APIs


## Apps metadata
This API retrieves the metadata for the registered apps. It receives as an input the URI of an APP, and generates a JSON-LD output that describes the input App using Dcat vocabulary.

The API is docker ready and can be run using the following command:

```
docker run -d --name platoon_ids_api -p 18877:5000 -e ENDPOINT='http://node2.research.tib.eu:51112/sparql' sdmtib/platoon_ids_api:2.3

```
The ENDPOINT parameter is the URL of the SPARQL endpoint that contains the Knowledge Gragh of the Apps.

Here is an example of a cURL request to generate the metadata related to the "PUPIN-RES-PROD" App

```
curl --location --request GET 'https://labs.tib.eu/sdm/platoon_metadata/get_apps_metadata?id=1' \
--header 'Content-Type: application/json' \
--data-raw '{
"dataset": "<https://w3id.org/platoon/entity/PUPIN-RES-PROD>"
}'
```

The generated output is:

```
{
    "@context": {
        "ids": "https://w3id.org/idsa/core/",
        "idsc": "https://w3id.org/idsa/code/",
        "part1": "https://im.internationaldataspaces.org/participant/part1",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "xsd": "http://www.w3.org/2001/XMLSchema#",
        "time": "http://www.w3.org/2006/time#",
        "dct": "http://purl.org/dc/terms/",
        "mls": "http://www.w3.org/ns/mls#",
        "dc": "http://purl.org/dc/elements/1.1/",
        "dcat": "http://www.w3.org/ns/dcat#"
    },
    "@type": "ids:AppResource",
    "@id": "https://w3id.org/platoon/entity/AnalyticalTool1",
    "ids:title": [
        {
            "@value": "Wind Turbine Digital Twin, Energy Conversion Normality Model",
            "@language": "en"
        }
    ],
    "ids:keywords": [
        {
            "@type": "ids:contentType",
            "@id": "Hybrid digital twin Physic-based digital twin"
        },
        {
            "@type": "ids:contentType",
            "@id": "DFIG"
        },
        {
            "@type": "ids:contentType",
            "@id": "Power converter"
        },
        {
            "@type": "ids:contentType",
            "@id": "IGBT"
        },
        {
            "@type": "ids:contentType",
            "@id": "Drive train"
        },
        {
            "@type": "ids:contentType",
            "@id": "Wind turbine"
        }
    ],
    "dc:hasVersion": {
        "@value": "0.1.0"
    },
    "dc:licence": {
        "@value": "ProprietaryTecnalia"
    },
    "dc:description": {
        "@value": "A hybrid digital twin based on wind turbine drivetrain physics based model. The app will mimic the behaviour of the wind turbine drive train electric elements (double fed induction generator DFIG and back-to-back power converter) during the energy conversion. This is based on a model that hybridizes a physical model and real operational SCADA data. Analytical methods used: Regression and Optimization.",
        "@language": "en"
    },
    "ids:appDocumentation": {
        "@value": "TBC in D4.3",
        "@language": "en"
    },
    "mls:hasInput": [
        "Wind speed (m/s)",
        "Pitch angle (degrees)",
        "Nacelle temperature (ºC)",
        "Winding temperature (ºC)"
    ],
    "mls:hasOutput": [
        "Generated active power (kW)",
        "Current RST (A)",
        "Voltage RST (V)",
        "Stator Winding Temperature (ºC)",
        "Optimized Wind Turbine Digital Twin Model"
    ],
    "mls:hasHyperParameter": [
        "Wind speed at nominal speed and at Cp max (m/s)",
        "Wind turbine inertia constant (s)",
        "Shaft spring constant factor (no unit)",
        "Shaft mutual damping (no unit)",
        "Stator widing resistance (pu)",
        "Rotor winding resistance (pu)",
        "Generator inertia constant (no unit)",
        "Generator friction factor (no unit)",
        "Power converter grid-side coupling resistance (pu)",
        "Power converter grid-side coupling inductance (pu)",
        "Converter line filter capacitor (VAr)",
        "DC bus voltage regulator gains (Kd, Ki)",
        "Speed regulator gains (no unit)"
    ],
    "mls:definedOn": [
        "Container Orchestrator (i.e. Kubernetes)",
        "Matlab",
        "Simulink"
    ],
    "dcat:contactPoint": [
        "ainhoa.pujana@tecnalia.com",
        "miguel.esteras@tecnalia.com"
    ]
}

```
