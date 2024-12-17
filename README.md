# Projeto AWS Lambda com API Gateway, DynamoDB e CloudWatch

Este projeto implementa uma arquitetura serverless utilizando AWS Lambda, API Gateway, DynamoDB e CloudWatch. A função Lambda recebe requisições HTTP pelo API Gateway, processa os dados e armazena informações no banco de dados DynamoDB. Logs detalhados são enviados para o CloudWatch para monitoramento e depuração.

## Pré-requisitos

1. **Configuração AWS:**
   - Uma conta AWS ativa.
   - Permissões necessárias para criar recursos no API Gateway, Lambda, DynamoDB e CloudWatch.

2. **Ambiente Local:**
   - Python 3.11 instalado.
   - Ferramentas de linha de comando da AWS (AWS CLI) configuradas.

3. **Dependências Python:**
   - Instale as bibliotecas requeridas listadas no arquivo `requirements.txt`.

## Arquitetura

A arquitetura inclui os seguintes componentes:

1. **API Gateway**: Responsável por receber as requisições HTTP e encaminhá-las para a função Lambda.
2. **Lambda**: Processa os dados recebidos e interage com o DynamoDB.
3. **DynamoDB**: Armazena os dados enviados pela Lambda.
4. **CloudWatch**: Monitora logs e métricas das execuções da Lambda.

<img width="443" alt="image" src="https://github.com/user-attachments/assets/57409e52-adcc-4f4e-9d77-6f1bc87284c4" />

## Estrutura do Projeto

```plaintext
project-root/
├── lambda_function.py  # Código principal da Lambda
├── requirements.txt    # Dependências do projeto
├── README.md           # Documentação do projeto
└── tests/              # Testes unitários
```

## Payload de Entrada

O payload de entrada esperado é um JSON com os seguintes campos:

```json
{
    "email": "test@example.com",
    "name": "Test User",
    "phone": "+1234567890",
    "password": "securepassword123"
}
```

## Código da Lambda

### Arquivo `lambda_function.py`

```python
import json
import boto3
import logging
import os
from botocore.exceptions import ClientError

# Configuração de logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    table_name = os.getenv("DYNAMODB_TABLE")
    table = dynamodb.Table(table_name)

    try:
        # Log da requisição recebida
        logger.info("Evento recebido: %s", json.dumps(event))

        # Validar o payload de entrada
        required_fields = ["email", "name", "phone", "password"]
        for field in required_fields:
            if field not in event:
                raise ValueError(f"Campo obrigatório ausente: {field}")

        # Inserir dados no DynamoDB
        item = {
            "email": event["email"],
            "name": event["name"],
            "phone": event["phone"],
            "password": event["password"]  # Em um caso real, isso deve ser criptografado
        }
        table.put_item(Item=item)

        # Resposta de sucesso
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Dados armazenados com sucesso."})
        }

    except ClientError as e:
        logger.error("Erro no DynamoDB: %s", e)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Erro ao acessar o DynamoDB."})
        }

    except ValueError as e:
        logger.error("Erro de validação: %s", e)
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(e)})
        }

    except Exception as e:
        logger.error("Erro inesperado: %s", e)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Erro interno do servidor."})
        }
```

## Configuração do DynamoDB

Crie uma tabela no DynamoDB com a seguinte configuração:

- **Nome da Tabela**: Defina um nome e configure-o como variável de ambiente na Lambda (`DYNAMODB_TABLE`).
- **Chave Primária**: `email` (String).

## Testes Locais

1. Instale as dependências no ambiente local:

   ```bash
   pip install -r requirements.txt
   ```

2. Use a biblioteca `pytest` para executar os testes unitários:

   ```bash
   pytest tests/
   ```

## Deploy

### 1. Criar Pacote ZIP

1. Instale as dependências no diretório do projeto:

   ```bash
   pip install -r requirements.txt -t .
   ```

2. Compacte os arquivos em um pacote ZIP:

   ```bash
   zip -r lambda_function.zip .
   ```

### 2. Subir para AWS Lambda

1. Vá ao Console da AWS Lambda.
2. Crie uma nova função Lambda ou edite uma existente.
3. Faça upload do arquivo ZIP criado.
4. Configure as variáveis de ambiente:
   - `DYNAMODB_TABLE`: Nome da tabela DynamoDB.

### 3. Configurar o API Gateway

1. Crie um novo recurso no API Gateway e integre-o com a Lambda.
2. Configure métodos (POST) para receber o payload de entrada.

## Monitoramento com CloudWatch

- Verifique logs no CloudWatch para monitorar execuções da Lambda e depurar problemas.

## Melhorias Futuras

- Criptografar a senha antes de armazená-la no DynamoDB.
- Adicionar autenticação ao API Gateway.
- Implementar validação mais robusta para os dados de entrada.


# Arquitetura do projeto
<img width="443" alt="image" src="https://github.com/user-attachments/assets/57409e52-adcc-4f4e-9d77-6f1bc87284c4" />
