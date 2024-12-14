import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('registration-table')

def lambda_handler(event, context):
    # Get request body
    print(event)
    
    try:

        # Create new item in DynamoDB table
        response = table.put_item(
            Item={
                'email': event['email'],
                'name': event['name'],
                'phone': event['phone'],
                'password': event['password']
            }
        )
        
        # Return response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({"message": "Registration successful"})
        }
    except Exception as e:
        print("Erro:", e)
        response = {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Ocorreu um erro.",
                "error": str(e)
            })
        }
        
    