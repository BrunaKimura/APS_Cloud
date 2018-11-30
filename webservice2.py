from flask import Flask, request
import requests
import boto3
import random
import json
import numpy as np
import threading
import time
import sys
import os

client = boto3.client('ec2')
ec2 = boto3.resource('ec2')

programa = sys.argv[0]
qtd = int(sys.argv[1])


def verifica_instancias():
    instance_iterator = client.describe_instances(
        Filters=[
            {
                'Name': 'tag:Owner',
                'Values': [
                    'Bruna',
                ],
            },
        ]
    )

    instacias = instance_iterator['Reservations']
    from pprint import pprint
    dicionario = {}
    if len(instacias) !=0:
        for i in instacias:
            for e in i['Instances']:
                status = str(e['State']['Name'])
                if status == 'running':
                    id_instacia= str(e['InstanceId'])
                    ip_publico = str(e['PublicIpAddress'])
                    dicionario[id_instacia] = ip_publico   

    else:
        print('Nao ha maquinas ativas')

    return dicionario



def ip_aleatorio(dicionario):
    ips = [ip for ip in dicionario.values()]
    ip_ale = np.random.choice(ips)
    return ip_ale



def acha_ip_db():
    ip_bruto = client.describe_instances(
        Filters=[
            {
                'Name': 'tag:Owner',
                'Values': [
                    'Banco'
                ],
            },
            {
                'Name': 'instance-state-name',
                    'Values':[
                        'running',
                        'pending'
                    ]
            },
        ]
    )
    instacias = ip_bruto['Reservations']
    if len(instacias) !=0:
        for i in instacias:
            for e in i['Instances']:
                ip_publico = str(e['PublicIpAddress'])

    return ip_publico

app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def catch_all(path):
    dicionario = verifica_instancias()
    maquina_ip = ip_aleatorio(dicionario)

    caminho = "http://"+maquina_ip + ":5000/"

    print(caminho)

    if request.method == 'GET':
        r = requests.get(caminho + path)
        return r.text

    elif request.method == 'POST':
        print(request.json)
        r = requests.post(caminho + path, json=request.json)
        return r.text

    elif request.method == 'PUT':
        r = requests.put(caminho + path, json=request.json)
        return r.text

    elif request.method == 'DELETE':
        r = requests.delete(caminho + path)
        return r.text

def destroi_instancia(id_i, client, ec2):
    deleta_instancia = client.terminate_instances(
        InstanceIds=[
            id_i,
        ]
    )
    print("Instância defeituosa deletada")


def cria_instancia(client, ec2, dif):
    describe = client.describe_security_groups(
        Filters=[
            {
                'Name': 'group-name',
                'Values': [
                    'APS2',
                ]
            },
        ]
    )

    idsg = str(describe['SecurityGroups'][0]['GroupId'])

    ip_db = acha_ip_db

    instance = ec2.create_instances(
        ImageId='ami-0ac019f4fcb7cb7e6',
        InstanceType='t2.micro',
        KeyName='apsbru',
        MaxCount=1,
        MinCount=1,
        SecurityGroupIds=[
            idsg
        ],
        SecurityGroups=[
            "APS2"
        ],
        UserData='''#!/bin/bash
                cd /home/ubuntu
                git clone https://github.com/BrunaKimura/APS_Cloud.git
                cd APS_Cloud
                export DB_HOST={0}
                chmod a+x install1.sh 
                ./install1.sh'''.format(ip_db),
        TagSpecifications=[
            {
                'ResourceType':'instance',
                'Tags': [
                    {
                        'Key': 'Owner',
                        'Value': 'Bruna'
                    },
                ]
            },
        ]
    )
    print("nova instancia criada")

def checa_health(dicionario, client, ec2, qtd):
    while True:
        chaves = list(dicionario.keys())
        tamanho = len(chaves)

        if tamanho>qtd:
            diff= tamanho-qtd
            while diff > 0:
                dif = tamanho-qtd
                destroi_instancia(chaves[0], client, ec2)
                time.sleep(300)
                dicionario = verifica_instancias()
                chaves = list(dicionario.keys())
                tamanho = len(chaves)
                diff=tamanho-qtd

        elif tamanho<qtd:
            dif = qtd-tamanho
            cria_instancia(client, ec2, dif)
            time.sleep(300)
            dicionario = verifica_instancias()

        for id_i in dicionario:
            caminho = "http://" + dicionario[id_i] + ":5000/healthcheck"
            try:
                r = requests.get(caminho, timeout=30)

                if r.status_code != 200:
                    print("erro na maquina!")
                    destroi_instancia(id_i, client, ec2)
                    cria_instancia(client, ec2, 1)
                    time.sleep(300)
                    dicionario = verifica_instancias() 
                else: 
                    print("tudo ok com a maquina:", id_i)

            except as e:
                print("tempo excedido")
                print (e)
                destroi_instancia(id_i,client, ec2)
                cria_instancia(client, ec2, 1)
                time.sleep(300)
                dicionario = verifica_instancias()

        time.sleep(20)


if __name__ == '__main__':
    dicionario = verifica_instancias()
    t = threading.Thread(target=checa_health, args=(dicionario,client, ec2, qtd))
    t.start()
    app.run(debug=True, host='0.0.0.0')