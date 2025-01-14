
![Banner](https://sistemadovarejo.com.br/assets/images/cupom_checkout.gif)

<h1>Sistema de Processamento de Notas Fiscais Eletrônicas</h1>
<p>

  Este projeto consiste na implementação de uma API REST em Python destinada a receber e processar imagens de notas fiscais eletrônicas em formato simplificado. O sistema utiliza Amazon Web Services (AWS) para o armazenamento e processamento das informações contidas nas notas fiscais, proporcionando uma solução eficiente e escalável.
</p>
<hr>


## 📈 Etapas do Projeto

| **Tarefas** | **Status** |
|-----------------|------------|
| 🌐 Desenvolver uma API REST em Python para receber um arquivo de nota fiscal e devolver as especificações detalhadas. <br> Usar a rota `/api/v1/invoice` com base nas notas da pasta dataset. | ✅ |
| ☁️ Armazenar o arquivo da nota fiscal em um bucket S3. | ✅ |
| 💾 Processar os dados da nota fiscal no bucket S3 com Textract e NLP (Spacy ou NLTK) para identificar elementos. | ✅ |
| 🤖 Aplicar uma LLM para formatar os dados de saída em JSON. | ✅ |
| 🗂️ Mover no bucket S3 as notas pagas em dinheiro/pix para a pasta "dinheiro" e outras formas para "outros". | ✅ |
| 📄 Retornar ao usuário os dados da nota fiscal. | ✅ |
---


## 🔧 Arquitetura 


![alt text](<assets/diagrama.png>)


---

## 💻 Tecnologias Utilizadas

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![HTML](https://img.shields.io/badge/HTML-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![Amazon AWS CDK](https://img.shields.io/badge/AWS%20CDK-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)
![Amazon AWS API Gateway](https://img.shields.io/badge/AWS%20API%20Gateway-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)
![Amazon AWS S3](https://img.shields.io/badge/AWS%20S3-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)
![Amazon AWS Lambda](https://img.shields.io/badge/AWS%20Lambda-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)
![Amazon AWS Textract](https://img.shields.io/badge/AWS%20Textract-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)
![Boto3](https://img.shields.io/badge/Boto3-4B8BBE?style=for-the-badge&logo=python&logoColor=white) 
![spaCy](https://img.shields.io/badge/spaCy-09A3D5?style=for-the-badge&logo=spacy&logoColor=white) 
![Hugging Face](https://img.shields.io/badge/Hugging%20Face-FFD700?style=for-the-badge&logo=huggingface&logoColor=white)
[![Google Colab](https://img.shields.io/badge/Google%20Colab-F9AB00?style=for-the-badge&logo=googlecolab&logoColor=white)](https://colab.research.google.com/)
![LLM](https://img.shields.io/badge/LLM-FF9900?style=for-the-badge&logo=ai&logoColor=white) 

---

## 📁 Estrutura de Pastas

```
Processamento-notas-fiscais-llm/
├── assets/
│   └── banner.jpg
├── cdk/
│   ├── cdk/
│   │   ├── __init__.py
│   │   └── cdk_stack.py
│   ├── lambda/
│   │   ├── llm_process.py
│   │   ├── process_textract.py
│   │   ├── requirements.txt
│   │   ├── spacy_service.py
│   │   └── upload_handler.py
│   └── tests/
│       └── unit/
│           ├── __init__.py
│           └── test_cdk_stack.py
├── .gitignore
├── app.py
├── cdk.json
├── prepare_layer.py
├── requirements-dev.txt
├── requirements.txt
├── source.bat
├── dataset/
│   └── NFs.zip
├── frontend/
│   ├── index.html
│   └── .gitignore
└── README.md
```
---

## 🤔 Como Utilizar

### Pré-requisitos:
1. Ter o AWS CDK instalado e configurado.
2. Ter as credenciais AWS configuradas no ambiente local.
3. Ter conta no Hugging Face.
4. Ter o Git baixado e configurado na máquina.
5. Ter o Python instalado e configurado na máquina (versão mínima: 3.11).

### Primeiros passos
1. Clone o repositório e entre na pasta:<br>
```bash
  git clone https://github.com/amandazzoc/Processamento-notas-fiscais-llm.git
  cd Processamento-notas-fiscais-llm
```
2. Acesse a branch:
```bash
git switch grupo-3
```
3. Coloque seu TOKEN do Hugging Face na linha 7 em ```cdk/lambda/llm_process.py```
```bash
headers = {"Authorization": "Bearer your_huggingface_api_key"}
```
#### Forma 1
##### Se quiser montar a arquitetura na sua conta AWS, siga as instruções:
1.  **Instalação de Dependências Spacy:** Execute o comando abaixo para criar o diretório lambda_layer com as dependências necessárias para serem incluídas na layer do Lambda.
```bash
  python prepare_layer
```
2. **Mude o nome das Buckets para evitar conflito:** Vá para ```cdk/cdk/cdk_stack.py``` e mude os nomes das buckets na linha 17 e 20
```bash   
  # Criar o bucket S3 para armazenamento de notas fiscais
  invoice_bucket = s3.Bucket(self, "InvoiceBucket", bucket_name="bucket-notas-fiscais-v2")

  # Criar o bucket S3 para armazenamento dos resultados
  result_bucket = s3.Bucket(self, "ResultBucket", bucket_name="bucket-notas-fiscais-v2-results")
```
3. **Entre no diretório do CDK**
```bash
  cd cdk
```
4. **Ative o ambiente virtual**
```bash
  # No Linux
  $ python -m venv .venv
  # No Windows
  % .venv\Scripts\activate.bat
```
5. **De o comando ```cdk bootstrap```.**
6. **Use o comando ```cdk deploy``` para criar os serviços necessários na sua conta da AWS:** O comando criará buckets S3 para armazenar as notas fiscais e os dados processados, além das funções Lambda para processar os documentos e a API Gateway para receber as solicitações. 
7. **Após fazer o deploy, no terminal aparecerá o seu link da API:** Vá para ```frontend/js/script.js``` e mude a linha que faz referencia ao link da API. (Mantenha a parte final da URL ```api/v1/invoice```)
```bash
  const response = await fetch("https://ak6bs6ep60.execute-api.us-east-1.amazonaws.com/prod/api/v1/invoice"
```
8. **Acesse o seu ```index.html``` pelo navegador e envie uma nota fiscal:** Após o envio deve retornar em formato JSON as informações principais da sua NF.
#### Forma 2
##### Se não tiver uma conta AWS e quiser apenas testar o nosso sistema, siga as instruções:
1. Apenas acesse o ```index.html``` pelo navegador e envie a nota fiscal. O processamento todo acontecerá na conta de um dos membros da nossa equipe e após processar, retornará em formato JSON as informações principais da sua NF.
2. Ou faça uma solicitação POST para o endpoint /api/v1/invoice, enviando a imagem da nota fiscal.
```bash
    curl --location --request POST 'http://ak6bs6ep60.execute-api.us-east-1.amazonaws.com/api/v1/invoice' --form 'file=@"<Nome do arquivo>"'
```

### Fluxo de Uso:
1) Implantação da Aplicação:

   - Para implantar a aplicação, execute os comandos a seguir a partir do diretório raiz do projeto.<br>
   O comando criará buckets S3 para armazenar as notas fiscais e os dados processados, além das funções Lambda para processar os documentos e a API Gateway para receber as solicitações.

```bash
    cdk deploy
```
  
2) Envio de uma Nota Fiscal:
   - Com a aplicação implantada, você pode enviar uma imagem de nota fiscal para o endpoint da API Gateway.
   - Para fazer isso, faça uma solicitação POST para o endpoint /api/v1/invoice, enviando a imagem da nota fiscal.
```bash
    curl --location --request POST 'http://<URL>/api/v1/invoice' --form 'file=@"<Nome do arquivo>"'
```

3) Processamento de Dados com AWS Textract, Spacy e Hugging Face(LLM):<br>
Após o upload, a função Lambda será acionada automaticamente para processar a nota fiscal utilizando as tecnologias sitadas.<br>

    - Extração com AWS Textract
    - Processamento NLP com spaCy
    - Refinamento do Texto com Hugging Face: Modelo: O texto extraído será refinado com o modelo Mistral-7B-Instruct-v0.2 da Hugging Face.
   ![alt text](assets/image-3.png)

   - O JSON gerado após o processamento completo:
   ![alt text](assets/image-2.png)

---

## 🚧 Dificuldades

| **Áreas**                                | **Descrição** |
|-----------------------------------------|---------------|
| **Configuração da API REST**            | O desenvolvimento de uma API REST em Python para receber e processar imagens exige uma <br> organização de código modular. |
| **Integração com o AWS S3**             | Armazenar arquivos no bucket S3 envolve a configuração adequada de permissões e credenciais. |
| **Extração de Texto com Amazon Textract** | A qualidade e o formato das notas fiscais podem variar, dificultando a extração de informações <br> consistentes com o Amazon Textract. |
| **Processamento de Linguagem Natural (NLP)** | Analisar e identificar elementos específicos da nota fiscal usando NLP (Spacy) foi desafiador, <br> devido ao tamanho da dependência encontramos dificuldades ao enviar os dados do Spacy para o Lambda. |
| **Aplicação de uma LLM para Formatação em JSON** | Dificuldades em encontrar um modelo LLM eficaz que, por meio de prompts, conseguisse <br> completar e formatar corretamente os campos em JSON. |
| **Organização e Estrutura do Código**   | Manter uma estrutura clara e organizada, separando as responsabilidades em diferentes módulos <br> e evitando duplicação de código. |

---


## 📚 Referências

| Tópicos | Descrição |
|--------|-----------|
|[Commits Semânticos](https://gist.github.com/alpteo/e93d754e5e09907c6362c4230fb66f87) | Mensagens de Commit Semântico com Emojis |
|[README](https://blog.rocketseat.com.br/como-fazer-um-bom-readme/) | Como fazer um bom README |
|[Emojis no README](https://dev.to/envoy_/150-badges-for-github-pnk) | Uso de emojis no README |
|[Emojipedia](https://emojipedia.org/check-mark) | Referência de emojis |
|[Analisando faturas e recibos](https://docs.aws.amazon.com/pt_br/textract/latest/dg/invoices-receipts.html) | Análise de faturas e recibos com Amazon Textract |
|[Analisando faturas e recibos com o Amazon Textract](https://docs.aws.amazon.com/pt_br/textract/latest/dg/analyzing-document-expense.html) | Análise de documentos de fatura e recebimento usando a API AnalyzeExpense |
|[Amazon Textract - Building a Receipt Processing Solution](https://github.com/raminetinati/aws-demo-textract-receipts) | Uso do Textract para gestão e análise de várias imagens |
|[Uploading Files to S3 Using API Gateway via Lambda Function](https://medium.com/@vaishnavipolichetti/uploading-files-to-s3-using-api-gateway-via-lambda-function-57fb160f7b7c) | Configurar endpoint no API Gateway para usar `filename` como chave no S3 via Lambda |
|[AWS Textract tutorial, Extract Forms, Tables from Image using Python](https://www.youtube.com/watch?v=xlUSJEsFQdk&t=274s) | Extração de Formulários e Tabelas com Textract usando Python |
|[Build a receipt and invoice processing pipeline with Amazon Textract](https://aws.amazon.com/pt/blogs/machine-learning/build-a-receipt-and-invoice-processing-pipeline-with-amazon-textract/) | Automatização de contas a pagar com Amazon Textract |
|[Finetune LLM to convert a receipt image to json or xml](https://mychen76.medium.com/finetune-llm-to-convert-a-receipt-image-to-json-or-xml-3f9a6237e991) | Conversão de imagens de recibo para JSON ou XML |
|[Pretrained Models](https://www.sbert.net/docs/sentence_transformer/pretrained_models.html#pretrained-models) | Modelos Transformadores de Frases na Hugging Face |

---

## Autores

<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/amandazzoc"><img src="https://avatars.githubusercontent.com/u/100137341?v=4" width="100px;" alt="Amanda Oliveira C"/><br /><sub><b>Amanda Oliveira C.</b></sub></a><br />
      </td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/MariaCaru"><img src="https://avatars.githubusercontent.com/u/127962556?v=4" width="100px;" alt="Maria Carolina C."/><br /><sub><b>Maria Carolina C.</b></sub></a><br />
      </td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/lilianecardeal"><img src="https://avatars.githubusercontent.com/u/143633881?v=4" width="100px;" alt="Liliane Cardeal"/><br /><sub><b>Liliane Cardeal</b></sub></a><br />
      </td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/munizeduardo"><img src="https://github.com/munizeduardo.png" width="100px;" alt="Eduardo Muniz"/><br /><sub><b>Eduardo Muniz</b></sub></a><br />
      </td>
    </tr>
  </tdbody>
</table>
