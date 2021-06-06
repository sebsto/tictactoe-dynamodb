# Copyright 2014. Amazon Web Services, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from boto3 import resource

try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen
import json

def getDynamoDBConnection(config=None, endpoint=None, local=False, use_instance_metadata=False):
    if local:
        db = resource('dynamodb',
            endpoint_url=endpoint,
            aws_secret_access_key='ticTacToeSampleApp',
            aws_access_key_id='ticTacToeSampleApp',
            use_ssl=False)
    else:
        params = {
            'use_ssl': True
            }

        # Read from config file, if provided
        if config is not None:
            if config.has_option('dynamodb', 'region'):
                params['region_name'] = config.get('dynamodb', 'region')
            if config.has_option('dynamodb', 'endpoint'):
                params['endpoint_url'] = config.get('dynamodb', 'endpoint')

            if config.has_option('dynamodb', 'aws_access_key_id'):
                params['aws_access_key_id'] = config.get('dynamodb', 'aws_access_key_id')
                params['aws_secret_access_key'] = config.get('dynamodb', 'aws_secret_access_key')

        # Use the endpoint specified on the command-line to trump the config file
        if endpoint is not None:
            params['endpoint_url'] = endpoint
            if 'region' in params:
                del params['region_name']

        # Only auto-detect the DynamoDB endpoint if the endpoint was not specified through other config
        if 'host' not in params and use_instance_metadata:
            response = urlopen('http://169.254.169.254/latest/dynamic/instance-identity/document').read()
            doc = json.loads(response);
            params['endpoint_url'] = f"https://dynamodb.{doc['region']}.amazonaws.com"
            params['region_name'] = doc['region']

        db = resource('dynamodb', **params)
    return db

def createGamesTable(db):

    try:
        gamesTable = db.create_table(
                    TableName="Games",
                    KeySchema=[ {
                        'AttributeName' : 'GameId',
                        'KeyType' : 'HASH'
                    }],
                    AttributeDefinitions=[
                        {
                            'AttributeName' : 'GameId',
                            'AttributeType' : 'S'
                        },
                        {
                            'AttributeName' : 'HostId',
                            'AttributeType' : 'S'
                        },
                        {
                            'AttributeName' : 'OpponentId',
                            'AttributeType' : 'S'
                        },
                        {
                            'AttributeName' : 'StatusDate',
                            'AttributeType' : 'S'
                        }
                    ],
                    BillingMode='PAY_PER_REQUEST'
                    ,GlobalSecondaryIndexes=[
                        {
                            'IndexName' : 'HostId-StatusDate-index',
                            'KeySchema' : [
                                {
                                    'AttributeName' : 'HostId',
                                    'KeyType' : 'HASH'
                                },
                                {
                                    'AttributeName' : 'StatusDate',
                                    'KeyType' : 'RANGE'
                                }
                            ],
                            'Projection': {
                                'ProjectionType': 'ALL'
                            }
                        },
                        {
                            'IndexName' : 'OpponentId-StatusDate-index',
                            'KeySchema' : [
                                {
                                    'AttributeName' : 'OpponentId',
                                    'KeyType' : 'HASH'
                                },
                                {
                                    'AttributeName' : 'StatusDate',
                                    'KeyType' : 'RANGE'
                                }
                            ],
                            'Projection': {
                                'ProjectionType': 'ALL'
                            }                            
                        }
                    ]
                )

    except Exception as dynamodberror:
        try:
            gamesTable = db.Table("Games")
        except Exception as e:
            print("Games Table doesn't exist.")
    finally:
        return gamesTable

#parse command line args for credentials and such
#for now just assume local is when args are empty
