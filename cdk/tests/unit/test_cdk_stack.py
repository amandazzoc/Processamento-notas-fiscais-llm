import aws_cdk as core
import aws_cdk.assertions as assertions
import pytest
import requests
import boto3
from aws_cdk.assertions import Match

from cdk.cdk_stack import CdkStack

# Fixtures para valores comuns
@pytest.fixture(scope="session")
def simple_template():
    app = core.App()
    stack = CdkStack(app, "cdk")
    template = assertions.Template.from_stack(stack)
    return template

@pytest.fixture
def api_url():
    return "https://q50iu93ri8.execute-api.us-east-1.amazonaws.com/prod/api/v1/invoice"

@pytest.fixture
def s3_client():
    return boto3.client('s3')

@pytest.fixture
def upload_file():
    return {'file': ('invoice.jpg', b'fake image content')}

@pytest.fixture
def s3_bucket():
    return "bucket-nf-g3"


# Teste para a conexão Lambda e bucket S3
def test_lambda_bucket_connection(simple_template):
    simple_template.has_resource_properties("AWS::IAM::Policy", Match.object_like({
        "PolicyDocument" : {
            "Statement": [
                {
                    "Resource": [
                        {
                            "Fn::GetAtt": [
                                Match.string_like_regexp("InvoiceBucket"),
                                "Arn"
                            ]
                        },
                        Match.any_value()
                    ]
                }
            ]
        }
    }))

# Teste para o runtime do Lambda
def test_lambda_runtime_with_matcher(simple_template):
    simple_template.has_resource_properties("AWS::Lambda::Function", {
        "Runtime": Match.string_like_regexp("python")
    })


# Função para upload de arquivo para a API
def upload_to_api(api_url, upload_file):
    return requests.post(api_url, files=upload_file)


# Teste da integração com a API Gateway e Lambda
def test_api_gateway_lambda_integration(api_url, upload_file):
    response = upload_to_api(api_url, upload_file)

    # Verificar se a resposta está correta
    assert response.status_code == 200
    assert response.json()['message'] == 'Arquivo enviado com sucesso!'

# Teste de headers CORS
def test_cors_headers(api_url):
    response = requests.options(api_url)

    # Verificar se os cabeçalhos CORS estão presentes
    assert response.headers.get('Access-Control-Allow-Origin') == '*'
    assert response.headers.get('Access-Control-Allow-Methods') == 'POST'
    assert response.headers.get('Access-Control-Allow-Headers') == 'Content-Type'

# Teste de integração com o S3
def test_integration_with_s3(api_url, s3_client, s3_bucket, upload_file):
    response = upload_to_api(api_url, upload_file)

    # Verificar se a resposta está correta
    assert response.status_code == 200

    # Verificar se o arquivo foi salvo no bucket S3
    response = s3_client.list_objects_v2(Bucket=s3_bucket)
    assert any(obj['Key'].startswith('invoice') for obj in response.get('Contents', []))
