import boto3
import json
import os
import logging
from spacy_service import process_text
from llm_process import refine_text
from upload_handler import upload_file

# Criar instância do logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Cliente Textract e S3
textract = boto3.client('textract')
s3 = boto3.client('s3')


def lambda_handler(event, context):
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type,file-name,Authorization",
        "Access-Control-Allow-Methods": "OPTIONS,POST",
        "Content-Type": "application/json"
    }

    try:
        # Salva o arquivo no bucket
        file = upload_file(event['body'])

        # Acessando o nome do bucket
        bucket_name = os.environ['INVOICE_BUCKET_NAME']

        # Acessando o nome do arquivo (key)
        file_key = file['file_name']

        print(f"Bucket: {bucket_name}, Arquivo: {file_key}")

        # Usando Textract para extrair o texto da imagem no S3
        response = textract.analyze_document(
            Document={
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name': file_key
                }
            },
            FeatureTypes=["FORMS", "TABLES"]  # Ou FeatureTypes=["TEXT"] para extração simples de texto
        )

        # Variável para armazenar o texto extraído
        extracted_text = ""

        # Percorrendo os blocos de texto do Textract
        for block in response['Blocks']:
            if block['BlockType'] == 'LINE':
                extracted_text += block['Text'] + "\n"

        logger.info(f"Texto extraído: {extracted_text}")

        # Pré-processa dados extraidos utilizando spaCy
        extracted_data = process_text(extracted_text)
        logger.info(extracted_data)

        # Nome do bucket de resultados (obtido da variável de ambiente)
        result_bucket_name = os.getenv("RESULT_BUCKET_NAME")

        # Envia dados processados para LLM para refinamento e adição de informações adicionais
        refined_output = refine_text(extracted_text, extracted_data)
        logger.info(refined_output)

        # Converte string para JSON
        refined_output_json = json.loads(refined_output)
        logger.info(refined_output_json)

        # Busca forma de pagamento de dentro do objeto JSON
        forma_de_pagamento = refined_output_json["forma_pgto"]
        logger.info(forma_de_pagamento)

        # Modifica nome do arquivo para salvar em formato JSON
        result_file_key = f"{file_key.split('/')[-1].replace('.jpg','')}-results.json"

        # Confere forma de pagamento para definir em qual path salvar
        if forma_de_pagamento.lower() == 'dinheiro' or forma_de_pagamento.lower() == 'pix':
          sorted_file = f"output/dinheiro/{result_file_key}"
        else:
          sorted_file = f"output/outros/{result_file_key}"

        # Gravar o texto extraído no bucket de resultados
        s3.put_object(
            Bucket=result_bucket_name,
            Key=sorted_file,
            Body=refined_output
        )

        # Retornando sucesso com o texto extraído
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'message': 'Texto extraído com sucesso!',
                'extracted_text': refined_output_json
            })
        }

    except KeyError as e:
        print(f"Chave faltando no evento: {e}")
        raise e

    except Exception as e:
        print(f"Erro inesperado: {e}")
        raise e
