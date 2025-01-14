import json
import boto3
import uuid
import base64
import os

s3 = boto3.client('s3')

def upload_file(file_body):
    try:
        # Gera um UUID para o nome do arquivo
        random_id = str(uuid.uuid4())
        bucket_name = os.environ['INVOICE_BUCKET_NAME']

        # Função espera receber a imagem em base64 no corpo da requisição
        body = json.loads(file_body)
        file_content_base64 = body.get('body', '')
        
        if not file_content_base64:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'POST'
                },
                'body': json.dumps({'message': 'Imagem não enviada.'})
            }

        # Decodificar a imagem base64
        file_content = base64.b64decode(file_content_base64)
        file_name = f"invoice-{random_id}.jpg"

        # Upload da imagem para o bucket S3
        s3.put_object(Bucket=bucket_name, Key=file_name, Body=file_content)

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # Cabeçalhos de CORS
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST'
            },
            'body': json.dumps({'message': 'Arquivo enviado com sucesso!'}),
            'file_name': file_name
        }

    except Exception as e:
        # Em caso de erro
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST'
            },
            'body': json.dumps({'message': f'Erro ao processar a requisição: {str(e)}'})
        }