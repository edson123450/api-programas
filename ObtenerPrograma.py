import boto3
import json

def lambda_handler(event,context):

    partition_key=event['body']['tenant_id']
    sort_key=event['body']['c_programa']

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
    response=tabla_programas.get_item(
        Key={
            'tenant_id':partition_key,
            'c_programa':sort_key
        }
    )
    response2=response['Item']['datos_programa']

    return {
        'statusCode':200,
        'response':response2
    }
