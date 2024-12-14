import json
import boto3
from moto import mock_aws
from lambda_function import lambda_handler


# Configurações do teste usando Moto
@mock_aws(config={"core": {"service_whitelist": ["dynamodb"]}})
def test_lambda_handler():
    # Configurar o mock do DynamoDB
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    
    # Criar a tabela mock
    table_name = "registration-table"
    dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {"AttributeName": "email", "KeyType": "HASH"}
        ],
        AttributeDefinitions=[
            {"AttributeName": "email", "AttributeType": "S"}
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 1,
            "WriteCapacityUnits": 1,
        }
    )
    
    # Configurar o evento simulado (entrada para a Lambda)
    event = {
        "email": "test@example.com",
        "name": "Test User",
        "phone": "+1234567890",
        "password": "securepassword123"
    }

    # Executar a função Lambda
    response = lambda_handler(event, None)

    # Validar a resposta
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["message"] == "Registration successful"

    # Validar o item no DynamoDB
    table = dynamodb.Table(table_name)
    item = table.get_item(Key={"email": event["email"]}).get("Item")
    assert item is not None
    assert item["email"] == event["email"]
    assert item["name"] == event["name"]
    assert item["phone"] == event["phone"]
    assert item["password"] == event["password"]
