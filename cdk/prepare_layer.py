import os
import subprocess
import shutil

def prepare_layer():
    # Criar diretório para o layer
    layer_dir = "lambda_layer/python"
    os.makedirs(layer_dir, exist_ok=True)
    
    # Instalar dependências no diretório do layer
    requirements_file = "lambda/requirements.txt"
    subprocess.check_call([
        "pip",
        "install",
        "-r", requirements_file,
        "-t", layer_dir,
        "--platform", "manylinux2014_x86_64",
        "--only-binary=:all:"
    ])

if __name__ == "__main__":
    prepare_layer()