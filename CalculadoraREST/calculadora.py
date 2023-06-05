import requests
import json
import sys

def get_operations():
    url = "http://ec2-3-133-82-159.us-east-2.compute.amazonaws.com:3000/calculadora/operacoes"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.text

def post_operation(operation, value1, value2):
    url = "http://ec2-3-133-82-159.us-east-2.compute.amazonaws.com:3000/calculadora/operacoes/" + operation + "/" + value1 + "/" + value2

    payload={}
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def validate_input(value1, value2):
    if is_float(value1):
        return True
    if is_float(value2):
        return True

    return False

def validateOperation(operation, operationsArray):
    if operation in operationsArray:
        return True
    
    return False

operations = json.loads(get_operations())
operationsArray = []

print("------ OPERACOES ------")

for op in operations: 
    print(op["endpoint"].split("calculadora/")[1])
    operationsArray.append(op["endpoint"].split("calculadora/")[1])

print("-----------------------")

operation = input("Digite o nome da operacao que deseja realizar: ")
if not validateOperation(operation, operationsArray):
    print("Operacao nao disponivel")
    sys.exit()

value1 = input("Defina o primeiro valor para realizar a operacao: ")
value2 = input("Defina o segundo valor para realizar a operacao: ")

if validate_input(value1, value2):
    resultado = json.loads(post_operation(operation, value1, value2))

    if type(resultado["value"]) == type(None):
        print("A calculadora não pode realizar a operacao para os valores fornecidos")
    else:
        print("Resultado = " + str(resultado["value"]))

else: 
    print("A calculadora não pode realizar a operacao para os valores fornecidos")