#!/bin/bash

# Script para instalar pacotes e bibliotecas necessárias para interagir com sensores e periféricos no Raspberry Pi

echo Atualizando o índice de pacotes...
sudo apt update -y
echo

echo Atualizando os pacotes...
sudo apt upgrade -y
echo

# Instala a biblioteca libgpiod2, que fornece uma API de usuário para GPIOs baseados no GPIO do kernel
echo Instalando biblioteca libgpiod2...
sudo apt install libgpiod2 -y
echo

# Instala o pacote python3-smbus, que fornece suporte ao I2C para o Python 3
echo Instalando pacote python3-smbus...
sudo apt install python3-smbus -y
echo

# Instala o pacote i2c-tools, que fornece ferramentas para trabalhar com dispositivos I2C
echo Instalando pacote i2c-tools...
sudo apt install i2c-tools -y
echo
