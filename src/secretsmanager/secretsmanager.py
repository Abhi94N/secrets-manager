# Use this code snippet in your app.
# If you need more information about configurations or implementing the sample code, visit the AWS docs:   
# https://aws.amazon.com/developers/getting-started/python/

import boto3
import json
import base64
from botocore.exceptions import ClientError
import logging
import logging.config
from os import path
import os

# 
log_file_path = path.join(path.dirname(path.abspath(__file__)), "logging_config.ini")
logging.config.fileConfig(log_file_path)
logger = logging.getLogger('secretsmanager')

class SecretsManager:
    
    def __init__(self, secret_name, region_name='us-west-2', host=''):
        self.region_name = region_name
        self.secret_name = secret_name
        self.db_secret = dict(self.get_db_secret(secret_name))
        if self.db_secret["host"] == '':
            self.db_secret["host"] = host
    
    @property
    def rds_connection_string(self):
        return f'postgresql://{self.db_secret["username"]}:{self.db_secret["password"]}@{self.db_secret["host"]}:{self.db_secret["port"]}/{self.db_secret["dbname"]}'

    def rds_connection(self, database):
        return f'postgresql://{self.db_secret["username"]}:{self.db_secret["password"]}@{self.db_secret["host"]}:{self.db_secret["port"]}/{database}'

    
    def get_db_secret(self, secret_name, region_name='us-west-2'):

        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )
        secret = ''

        # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
        # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        # We rethrow the exception by default.
        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
            logger.debug(f'Fetched Secret: {get_secret_value_response}')
            
            logger.info(f'Secret Recieved Status: %s\n Request ID: %s' % (get_secret_value_response["ResponseMetadata"]["HTTPStatusCode"], get_secret_value_response["ResponseMetadata"]["RequestId"]) )
        except ClientError as e:
            if e.response['Error']['Code'] == 'DecryptionFailureException':
                # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response['Error']['Code'] == 'InternalServiceErrorException':
                # An error occurred on the server side.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                # You provided an invalid value for a parameter.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                # You provided a parameter value that is not valid for the current state of the resource.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response['Error']['Code'] == 'ResourceNotFoundException':
                # We can't find the resource that you asked for.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
        else:
            # Decrypts secret using the associated KMS key.
            # Depending on whether the secret is a string or binary, one of these fields will be populated.
            
            if 'SecretString' in get_secret_value_response:
                secret = get_secret_value_response['SecretString']
            else:
                secret = base64.b64decode(get_secret_value_response['SecretBinary'])

        finally:
            return json.loads(secret) if secret != '' else {'engine': '', 'username': '', 'password': '', 'dbname': '', 'port': '', 'host': ''}



    