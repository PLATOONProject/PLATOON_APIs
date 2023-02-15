#!/usr/bin/env python3
#
# Description: POST service for exploration of
# data of Lung Cancer in the iASiS KG.
#

import sys
from flask import Flask, abort, request, make_response , render_template
import json
from SPARQLWrapper import SPARQLWrapper, JSON, POST
import logging
import os
from flask_cors import CORS


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)




KG = os.environ["ENDPOINT"]
#KG= 'http://node2.research.tib.eu:51112/sparql'
EMPTY_JSON = "{}"

app = Flask(__name__)
CORS(app)


############################
#
# Query constants
#
############################


APPS_DESCRIPTION_QUERY="""
prefix ids: <https://w3id.org/idsa/core/> 
prefix dc: <http://purl.org/dc/elements/1.1/>
prefix mls: <http://www.w3.org/ns/mls#>
SELECT DISTINCT ?title ?version ?licence  ?description ?documentation  WHERE
{{
<{0}> a ids:App.
OPTIONAL {{
<{0}> ids:title ?title.
}}
OPTIONAL {{
<{0}> dc:hasVersion ?version.
}}
OPTIONAL {{
<{0}> dc:licence ?licence.
}}
OPTIONAL {{
<{0}> dc:description ?description.
}}
OPTIONAL {{
<{0}> ids:appDocumentation ?documentation.
}}
}}
"""


APPS_PROPERTY_QUERY="""
prefix ids: <https://w3id.org/idsa/core/> 
prefix dc: <http://purl.org/dc/elements/1.1/>
prefix mls: <http://www.w3.org/ns/mls#>
SELECT DISTINCT ?p_values  WHERE
{{
<{0}> {1} ?p_values.
}}
"""



DATASET_PROPERTIES_QUERY="""
SELECT DISTINCT ?title ?type ?publisher ?language ?accessRights ?temporalResolution WHERE 
{{
{0} a ?type.
OPTIONAL {{
{0} <https://w3id.org/idsa/core/title> ?title.
}}
OPTIONAL {{
{0} <https://w3id.org/idsa/core/publisher> ?publisher.
}}
OPTIONAL {{
{0} <https://w3id.org/idsa/core/language> ?language.
}}
OPTIONAL {{
{0} <https://w3id.org/idsa/core/permission> ?accessRights.
}}
OPTIONAL {{
{0} <https://w3id.org/idsa/core/temporalResolution> ?temporalResolution.
}}
}}
"""

DATASET_CONTENT_TYPE_QUERY="""
SELECT DISTINCT ?contentType WHERE 
{{
{0} <https://w3id.org/idsa/core/type> ?contentType
}}
"""

DATASET_IDS="""
{{
	"@context": {{
    "ids": "https://w3id.org/idsa/core/",
    "idsc": "https://w3id.org/idsa/code/",
    "part1": "https://im.internationaldataspaces.org/participant/part1",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "time": "http://www.w3.org/2006/time#",
    "dct": "http://purl.org/dc/terms/"
  }},
    "@type": "{0}",
    "@id": "{1}",
    "title": [{{
            "@value": "{2}",
            "@language": "en"
        }}
    ],
	"types": [{3}]
    ,
    "publisher": {{"@value": "{4}"}},
    "language": {{
        "@type": "ids:Language",
        "@id": "{5}"
    }},
	"accessRights":{{
			"@value": "{6}",
	}},
	"temporalResolution":{{ 
			"@value": "{7}",
	}}
}}
    """


APPS_METADATA="""
{{
	"@context": {{
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
  }},
    "@type": "ids:AppResource",
    "@id": "{0}",
    "ids:title": [{{
            "@value": "{1}",
            "@language": "en"
        }}
    ],
	"ids:keywords": [{2}]
    ,
    "dc:hasVersion": {{"@value": "{3}"}},
    "dc:licence": {{"@value": "{4}"}},
	"dc:description":{{
			"@value": "{5}",
            "@language": "en"
	}},
    "ids:appDocumentation":{{
			"@value": "{6}",
            "@language": "en"
	}},
	"mls:hasInput": {7},
    "mls:hasOutput": {8},
    "mls:hasHyperParameter": {9},
    "mls:definedOn": {10},
    "dcat:contactPoint": {11}
}}
    """


############################
#
# Query generation
#
############################


def execute_query(query):
    sparql_ins = SPARQLWrapper(KG)
    sparql_ins.setMethod(POST)
    sparql_ins.setQuery(query)
    sparql_ins.setReturnFormat(JSON)
    return sparql_ins.query().convert()['results']['bindings']



############################
#
# Processing results
#
############################

def get_apps_description_query(app_id):
    query=APPS_DESCRIPTION_QUERY.format(app_id)      
    qresults = execute_query(query)
    return qresults


def get_ids_description_query(ids_dataset):
    query=DATASET_PROPERTIES_QUERY.format(ids_dataset)      
    qresults = execute_query(query)
    return qresults

def get_ids_types_query(ids_dataset):
    query=DATASET_CONTENT_TYPE_QUERY.format(ids_dataset)      
    qresults = execute_query(query)
    return qresults



def get_apps_properties_query(app_id,property_):
    query=APPS_PROPERTY_QUERY.format(app_id,property_)      
    qresults = execute_query(query)
    return qresults

#response_query[0]['classType']['value'],

def proccesing_response(input_list):
    ids_dataset=input_list["dataset"]
    response=dict()
    dataset_properties_query_response = get_ids_description_query(ids_dataset)
    if 'title' not in dataset_properties_query_response[0]:
        dataset_properties_query_response[0]['title']={}
        dataset_properties_query_response[0]['title']['value']=""
    if 'publisher' not in dataset_properties_query_response[0]:
        dataset_properties_query_response[0]['publisher']={}
        dataset_properties_query_response[0]['publisher']['value']=""
    if 'language' not in dataset_properties_query_response[0]:
        dataset_properties_query_response[0]['language']={}
        dataset_properties_query_response[0]['language']['value']=""
    if 'accessRights' not in dataset_properties_query_response[0]:
        dataset_properties_query_response[0]['accessRights']={}
        dataset_properties_query_response[0]['accessRights']['value']=""
    if 'temporalResolution' not in dataset_properties_query_response[0]:
        dataset_properties_query_response[0]['temporalResolution']={}
        dataset_properties_query_response[0]['temporalResolution']['value']=""
    
    dataset_types_query_response = get_ids_types_query(ids_dataset)
    contentTypes=""
    for item in dataset_types_query_response:
        contentTypes+="""{ "@type": "ids:contentType",
        "@id": \""""+item['contentType']['value']+"\"},"
    contentTypes=contentTypes[:-1]
    response['IDS']=DATASET_IDS.format(
            dataset_properties_query_response[0]['type']['value'],
            ids_dataset,
            dataset_properties_query_response[0]['title']['value'],
            contentTypes,
            dataset_properties_query_response[0]['publisher']['value'],
            dataset_properties_query_response[0]['language']['value'],
            dataset_properties_query_response[0]['accessRights']['value'],
            dataset_properties_query_response[0]['temporalResolution']['value']
            )
    

    return response['IDS']

def proccesing_response_apps(app_id):
    app_id="https://w3id.org/platoon/entity/AnalyticalTool"+app_id
    response=dict()
    apps_properties_query_response = get_apps_description_query(app_id)
    if 'title' not in apps_properties_query_response[0]:
        apps_properties_query_response[0]['title']={}
        apps_properties_query_response[0]['title']['value']=""
    if 'version' not in apps_properties_query_response[0]:
        apps_properties_query_response[0]['version']={}
        apps_properties_query_response[0]['version']['value']=""
    if 'licence' not in apps_properties_query_response[0]:
        apps_properties_query_response[0]['licence']={}
        apps_properties_query_response[0]['licence']['value']=""
    if 'description' not in apps_properties_query_response[0]:
        apps_properties_query_response[0]['description']={}
        apps_properties_query_response[0]['description']['value']=""
    if 'documentation' not in apps_properties_query_response[0]:
        apps_properties_query_response[0]['documentation']={}
        apps_properties_query_response[0]['documentation']['value']=""
   

    app_input=get_apps_properties_query(app_id,"mls:hasInput")
    app_output=get_apps_properties_query(app_id,"mls:hasOutput")
    app_hyper=get_apps_properties_query(app_id,"mls:hasHyperParameter")
    app_requirement=get_apps_properties_query(app_id,"mls:definedOn")
    app_contact=get_apps_properties_query(app_id,"ids:publisher")
    app_keywords=get_apps_properties_query(app_id,"ids:keyword")
    


        
    contentTypes=""    
    for item in app_keywords:
        contentTypes+="""{ "@type": "ids:contentType",
        "@id": \""""+item['p_values']['value']+"\"},"
    contentTypes=contentTypes[:-1]
    
    
    response['APP_METADATA']=APPS_METADATA.format(
            app_id,
            apps_properties_query_response[0]['title']['value'],
            contentTypes,
            apps_properties_query_response[0]['version']['value'],
            apps_properties_query_response[0]['licence']['value'],
            apps_properties_query_response[0]['description']['value'],
            apps_properties_query_response[0]['documentation']['value'],
            json.dumps([x['p_values']['value'] for x in app_input]),
            json.dumps([x['p_values']['value'] for x in app_output]),
            json.dumps([x['p_values']['value'] for x in app_hyper]),
            json.dumps([x['p_values']['value'] for x in app_requirement]),
            json.dumps([x['p_values']['value'] for x in app_contact]),
            )
    

    return response['APP_METADATA']


@app.route('/get_ids_description', methods=['POST'])
def get_ids_description():
    if (not request.json):
        abort(400)
    input_list = request.json
    if len(input_list) == 0:
        logger.info("Error in the input format")
        response = "{results: 'Error in the input format'}"
    else:
        response = proccesing_response(input_list)       
        #r = json.dumps(response, indent=4)  
    logger.info("Sending the results: ")
    response = make_response(response, 200)
    response.mimetype = "application/json"
    return response


@app.route('/get_apps_metadata', methods=['GET'])
def get_apps_metadata():
    app_id = request.args.get('id')
    if app_id == "":
        logger.info("Error in the input")
        response = "{results: 'Error in the input'}"
    else:
        response = proccesing_response_apps(app_id)       
        #r = json.dumps(response, indent=4)  
    logger.info("Sending the results: ")
    response = make_response(response, 200)
    response.mimetype = "application/json"
    return response





def main(*args):
    if len(args) == 1:
        myhost = args[0]
    else:
        myhost = "0.0.0.0"
    app.run(debug=False, host=myhost)
    
if __name__ == '__main__':
     main(*sys.argv[1:])
