# PLATOON_APIs

The APIs are docker ready and can be run using the following command:

```
docker run -d --name platoon_ids_api -p 18877:5000 -e ENDPOINT='http://node2.research.tib.eu:51112/sparql' sdmtib/platoon_ids_api:2.3

```
The ENDPOINT parameter is the URL of the SPARQL endpoint that contains the Knowledge Gragh of the Apps.

## Apps metadata API
This API retrieves the metadata for the registered apps. It receives as an input the ID of an APP, and generates a JSON-LD output that describes the input App using Dcat vocabulary.



Here is an example of a cURL request to generate the metadata related to the App 1

```
curl --location --request GET 'https://labs.tib.eu/sdm/platoon_metadata/get_apps_metadata?id=1'
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

## Datasets Description API

This API retrieves the description of dataset in the PLATOON project. It receives as an input the URI of a dataset, and generates as an output a JSON-LD that describes the dataset using the Dcat vocabulary.

Here is an example of a cURL request to generate the metadata related to the "PUPIN-RES-PROD" dataset

```
curl --location --request POST 'https://labs.tib.eu/sdm/platoon_metadata/get_ids_description' \
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
        "dct": "http://purl.org/dc/terms/"
    },
    "@type": "https://w3id.org/idsa/core/Resource",
    "@id": "<https://w3id.org/platoon/entity/PUPIN-RES-PROD>",
    "title": [
        {
            "@value": "Historical Wind Power Production Measurements",
            "@language": "en"
        }
    ],
    "types": [
        {
            "@type": "ids:contentType",
            "@id": "http://www.w3.org/2006/time#Interval"
        },
        {
            "@type": "ids:contentType",
            "@id": "http://www.w3.org/2006/time#TemporalEntity"
        },
        {
            "@type": "ids:contentType",
            "@id": "http://www.w3.org/2006/time#Instant"
        },
        {
            "@type": "ids:contentType",
            "@id": "https://w3id.org/seas/FeatureOfInterest"
        },
        {
            "@type": "ids:contentType",
            "@id": "https://w3id.org/platoon/WindFarm"
        },
        {
            "@type": "ids:contentType",
            "@id": "https://w3id.org/seas/ElectricPowerSystem"
        },
        {
            "@type": "ids:contentType",
            "@id": "https://w3id.org/seas/ElectricPowerProducer"
        },
        {
            "@type": "ids:contentType",
            "@id": "http://www.semanticweb.org/ontologies/2011/9/Ontology1318785573683.owl#WindTurbine"
        },
        {
            "@type": "ids:contentType",
            "@id": "http://www.iec.ch/TC57/CIM#WindGeneratingUnit"
        },
        {
            "@type": "ids:contentType",
            "@id": "http://www.iec.ch/TC57/CIM#WindPlantIEC"
        },
        {
            "@type": "ids:contentType",
            "@id": "https://w3id.org/platoon/OffshoreWindTurbine"
        },
        {
            "@type": "ids:contentType",
            "@id": "http://www.iec.ch/TC57/CIM#GeneratingUnit"
        },
        {
            "@type": "ids:contentType",
            "@id": "http://www.iec.ch/TC57/CIM#Plant"
        },
        {
            "@type": "ids:contentType",
            "@id": "https://w3id.org/platoon/AirTemperatureProperty"
        },
        {
            "@type": "ids:contentType",
            "@id": "https://w3id.org/platoon/AirTemperatureEvaluation"
        },
        {
            "@type": "ids:contentType",
            "@id": "https://w3id.org/seas/WindDirectionProperty"
        },
        {
            "@type": "ids:contentType",
            "@id": "http://www.semanticweb.org/ontologies/2011/9/Ontology1318785573683.owl#WindDirection"
        },
        {
            "@type": "ids:contentType",
            "@id": "https://w3id.org/seas/WindDirectionEvaluation"
        },
        {
            "@type": "ids:contentType",
            "@id": "https://w3id.org/platoon/WeatherStation"
        },
        {
            "@type": "ids:contentType",
            "@id": "https://w3id.org/platoon/ForecastOfElectricProductionProperty"
        },
        {
            "@type": "ids:contentType",
            "@id": "https://w3id.org/platoon/ForecastOfActivePower"
        },
        {
            "@type": "ids:contentType",
            "@id": "https://w3id.org/seas/ElectricPowerProperty"
        },
        {
            "@type": "ids:contentType",
            "@id": "https://saref.etsi.org/core/Power"
        },
        {
            "@type": "ids:contentType",
            "@id": "http://www.iec.ch/TC57/CIM#ActivePower"
        },
        {
            "@type": "ids:contentType",
            "@id": "https://w3id.org/platoon/ForecastOfActivePowerEvaluation"
        },
        {
            "@type": "ids:contentType",
            "@id": "https://w3id.org/platoon/ForecastOfElectricPowerEvaluation"
        },
        {
            "@type": "ids:contentType",
            "@id": "https://w3id.org/seas/ElectricPowerEvaluation"
        },
        {
            "@type": "ids:contentType",
            "@id": "https://w3id.org/platoon/ActivePowerEvaluation"
        },
        {
            "@type": "ids:contentType",
            "@id": "https://w3id.org/platoon/SolarInsolationProperty"
        },
        {
            "@type": "ids:contentType",
            "@id": "https://w3id.org/seas/PressureProperty"
        },
        {
            "@type": "ids:contentType",
            "@id": "http://www.semanticweb.org/ontologies/2011/9/Ontology1318785573683.owl#Pressure"
        },
        {
            "@type": "ids:contentType",
            "@id": "https://w3id.org/seas/PressureEvaluation"
        },
        {
            "@type": "ids:contentType",
            "@id": "https://w3id.org/seas/WindSpeedProperty"
        },
        {
            "@type": "ids:contentType",
            "@id": "https://w3id.org/seas/WindSpeedEvaluation"
        }
    ],
    "publisher": {
        "@value": "IMP"
    },
    "language": {
        "@type": "ids:Language",
        "@id": "http://id.loc.gov/vocabulary/iso639-1/ENG"
    },
    "accessRights": {
        "@value": "Private",
    },
    "temporalResolution": {
        "@value": "could cover period of couple of previous years",
    }
}
```

