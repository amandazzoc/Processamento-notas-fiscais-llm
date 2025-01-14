import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_iam as iam
)
from constructs import Construct

class CdkStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Criar o bucket S3 para armazenamento de notas fiscais
        invoice_bucket = s3.Bucket(self, "InvoiceBucket", bucket_name="bucket-notas-fiscais-v2")

        # Criar o bucket S3 para armazenamento dos resultados
        result_bucket = s3.Bucket(self, "ResultBucket", bucket_name="bucket-notas-fiscais-v2-results")

        # Criação do Lambda Layer com as dependências
        dependencies_layer = _lambda.LayerVersion(
            self, 'DependenciesLayer',
            code=_lambda.Code.from_asset('lambda_layer'),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_12],
            description='Layer containing spacy and other dependencies'
        )

        # Cria a função Lambda para processar o Textract
        lambda_function_textract = _lambda.Function(
            self, "TextractFunction",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="process_textract.lambda_handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={
                "INVOICE_BUCKET_NAME": invoice_bucket.bucket_name,
                "RESULT_BUCKET_NAME": result_bucket.bucket_name  # Passa o nome do bucket de resultados para o Lambda
            },
            layers=[dependencies_layer],
            timeout=cdk.Duration.seconds(90)
        )

        # Permitir que a função Lambda de upload escreva no bucket de notas fiscais
        invoice_bucket.grant_write(lambda_function_textract)

        # Criar a API Gateway para a função de upload
        api = apigateway.LambdaRestApi(
            self, "InvoiceApi",
            handler=lambda_function_textract,
            proxy=False
        )

        # Definir a rota para upload
        invoices_resource = api.root.add_resource("api").add_resource("v1").add_resource("invoice")
        invoices_resource.add_method(
            "POST",
            apigateway.LambdaIntegration(lambda_function_textract),
            method_responses=[
                {
                    "statusCode": "200",
                    "responseParameters": {
                        "method.response.header.Access-Control-Allow-Origin": True,
                        "method.response.header.Access-Control-Allow-Headers": True,
                        "method.response.header.Access-Control-Allow-Methods": True,
                    }
                }
            ]
        )

        # Habilitar CORS diretamente no método POST
        invoices_resource.add_cors_preflight(
            allow_origins=["*"],
            allow_methods=["POST"],
            allow_headers=["Content-Type"],
        )

        # Permitir que o Lambda Textract leia do bucket de notas fiscais
        invoice_bucket.grant_read(lambda_function_textract)

        # Permitir que o Lambda Textract escreva no bucket de resultados
        result_bucket.grant_write(lambda_function_textract)

        # Adicionar permissões para o Textract
        lambda_function_textract.add_to_role_policy(
            iam.PolicyStatement(
                actions=["textract:AnalyzeDocument", "textract:DetectDocumentText"],
                resources=["*"]
            )
        )
