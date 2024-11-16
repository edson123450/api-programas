import boto3
from boto3.dynamodb.conditions import Key
import json

def lambda_handler(event,context):

    partition_key=event['body']['tenant_id']
    #sort_key=event['body']['c_programa']
    #datos_programa=event['body']['datos_programa']

    # Inicio - Proteger el Lambda
    token = event['headers']['Authorization']
    lambda_client = boto3.client('lambda')
    payload_string = '{ "token": "' + token + '" }'
    invoke_response = lambda_client.invoke(
        FunctionName="ValidarTokenEstudiante",
        InvocationType='RequestResponse',
        Payload=payload_string
    )
    response = json.loads(invoke_response['Payload'].read())
    print(response)
    if response['statusCode'] == 403:
        return {
            'statusCode': 403,
            'status': 'Forbidden - Acceso no autorizado'
        }
    # Fin - Proteger el Lambda

    dynamodb=boto3.resource('dynamodb')
    tabla_programas=dynamodb.Table('tabla_programas')

    response=tabla_programas.query(
        KeyConditionExpression=Key('tenant_id').eq(partition_key)
    )

    items=response['Items']
    numero_registros=response['Count']

    return {
        'statusCode':200,
        'tenant_id':partition_key,
        'numero_registros':numero_registros,
        'programas':items
    }