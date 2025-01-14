import re
import spacy

# Carregar modelo em branco SpaCy
nlp = spacy.blank("pt")

# Função de processamento para extração dos dados
def process_text(text_data):
  # Dicionário para armazenar os dados extraídos
  extracted_data = {
      "nome_emissor": "",
      "CNPJ_emissor": "",
      "endereco_emissor": "",
      "CNPJ_CPF_consumidor": "",
      "data_emissao": "",
      "numero_nota_fiscal": "",
      "serie_nota_fiscal": "",
      "valor_total": "",
      "forma_pgto": ""
  }

  # Padrões de regex para os campos específicos
  patterns = {
      "cnpj": r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}",
      "cpf": r"\d{3}\.\d{3}\.\d{3}-\d{2}",
      "data": r"\d{2}/\d{2}/\d{4}",
      "numero_nota_fiscal": r"NFe\s?\d+",
      "serie_nota_fiscal": r"Serie\s?\d+",
      "forma_pgto": r"(?:Forma\sde\sPagamento|Pagamento|Pgto|Pago\sem)[:\s]*(dinheiro|pix|cart[aã]o|débito|credito|cheque)",
      "valor_total": r"Valor(?: Total)?[:\s]*([\d.,]+)",
  }

  # Processamento NLP com SpaCy

  doc = nlp(text_data)
  for ent in doc.ents:
      if ent.label_ == "NOME" and not extracted_data["nome_emissor"]:
          extracted_data["nome_emissor"] = ent.text
      elif ent.label_ == "CNPJ" and not extracted_data["CNPJ_emissor"]:
          extracted_data["CNPJ_emissor"] = ent.text
      elif ent.label_ == "CEP" and not extracted_data["endereco_emissor"]:
          extracted_data["endereco_emissor"] = ent.text
      elif ent.label_ == "CPF" and not extracted_data["CNPJ_CPF_consumidor"]:
          extracted_data["CNPJ_CPF_consumidor"] = ent.text
      elif ent.label_ == "DATA" and not extracted_data["data_emissao"]:
          extracted_data["data_emissao"] = ent.text
      elif ent.label_ == "NOTAFISCAL" and not extracted_data["numero_nota_fiscal"]:
          extracted_data["numero_nota_fiscal"] = ent.text
      elif ent.label_ == "SERIE" and not extracted_data["serie_nota_fiscal"]:
          extracted_data["serie_nota_fiscal"] = ent.text
      elif ent.label_ == "VALOR" and not extracted_data["valor_total"]:
          extracted_data["valor_total"] = ent.text
      elif ent.label_ == "PAGAMENTO" and not extracted_data["forma_pgto"]:
          extracted_data["forma_pgto"] = ent.text



  # Usando regex para identificar os campos com padrão específico
  for key, pattern in patterns.items():
      match = re.search(pattern, text_data)
      if match:
          if key == "cnpj":
              extracted_data["CNPJ_emissor"] = match.group()
          elif key == "cpf":
              extracted_data["CNPJ_CPF_consumidor"] = match.group()
          elif key == "data":
              extracted_data["data_emissao"] = match.group()
          elif key == "numero_nota_fiscal":
              extracted_data["numero_nota_fiscal"] = match.group().replace("NFe", "").strip()
          elif key == "serie_nota_fiscal":
              extracted_data["serie_nota_fiscal"] = match.group().replace("Serie", "").strip()
          elif key == "forma_pgto":
              extracted_data["forma_pgto"] = match.group()
          elif key == "valor_total" and not extracted_data["valor_total"]:
              extracted_data["valor_total"] = match.group()

  return extracted_data