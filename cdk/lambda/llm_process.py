import requests

# URL da API da Hugging Face
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

# Cabeçalhos para autenticação (substitua 'your_huggingface_api_key' pela sua chave de API da Hugging Face)
headers = {"Authorization": "Bearer your_huggingface_api_key"}

def refine_text(invoice_text, extracted_data):
  # Criar o prompt para o modelo
  prompt = f"""
  Texto do invoice:
  '{invoice_text}'

  Your task is to complete the JSON object's missing fields.

  Exemplo de output:
  {extracted_data}
  Please fill in all fields based on the text of the invoice. If you can't find some fields in the text, fill them with "None".
  Just return the output as in the example above and nothing else. Make sure the result is a valid JSON object, use double quotes.
  ^^^
  """

  # Payload para a requisição
  payload = {
      "inputs": prompt,
      "parameters": {
          "max_new_tokens": 500  # Número máximo de tokens para o output
      }
  }
  # Enviar a requisição para a API da Hugging Face
  response = requests.post(API_URL, headers=headers, json=payload)

  if response.status_code == 200:
    # Extrair e imprimir apenas o JSON gerado pelo modelo
    result = response.json()
    output_text = result[0]['generated_text']

    plus_index = output_text.find("^^^")

    formatted_text = output_text[plus_index + 3:].strip()

    # Trocar aspas simples por aspas duplas para deixar objeto JSON válido
    new_string = formatted_text.replace("'", '"')

    # Exibir apenas o JSON gerado após o símbolo "^^^"
    if plus_index != -1:
        return new_string
    else:
        return "Símbolo '^^^' não encontrado no output."
  else:
      print(f"Erro na requisição: {response.status_code}")
      print(response.text)
