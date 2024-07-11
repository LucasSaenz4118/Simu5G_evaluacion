#!/bin/bash

# Variables de URLs y archivos
OMNETPP_URL="https://github.com/omnetpp/omnetpp/releases/download/omnetpp-6.0/omnetpp-6.0-linux-x86_64.tgz"
INET_URL="https://github.com/LucasSaenz4118/Simu5G/raw/main/Complementos/inet-4.5.2-scr.tgz"
SIMU5G_URL="https://github.com/LucasSaenz4118/Simu5G/raw/main/Complementos/Simu5G-1.2.2.zip"
VEINS_URL="https://github.com/LucasSaenz4118/Simu5G/raw/main/Complementos/veins-5.2.zip"

OMNETPP_FILE="omnetpp-6.0-linux-x86_64.tgz"
INET_FILE="inet-4.5.2-scr.tgz"
SIMU5G_FILE="Simu5G-1.2.2.zip"
VEINS_FILE="veins-5.2.zip"

# Directorios de instalación
INSTALL_DIR=$HOME/omnetpp
INET_DIR=$INSTALL_DIR/inet4
SIMU5G_DIR=$INSTALL_DIR/Simu5G
VEINS_DIR=$INSTALL_DIR/veins

# Paso 1: Crear directorio de instalación
mkdir -p $INSTALL_DIR
cd $INSTALL_DIR

# Paso 2: Descargar y descomprimir OMNeT++
echo "Descargando y descomprimiendo OMNeT++..."
wget $OMNETPP_URL -O $OMNETPP_FILE
tar xvfz $OMNETPP_FILE

# Paso 3: Configurar variables de entorno para OMNeT++
echo "Configurando variables de entorno para OMNeT++..."
cd omnetpp-6.0
source setenv
echo 'if [ -f "$HOME/omnetpp-6.0/setenv" ]; then source "$HOME/omnetpp-6.0/setenv"; fi' >> ~/.profile

# Paso 4: Configurar y compilar OMNeT++
echo "Configurando y compilando OMNeT++..."
./configure
make -j8

# Paso 5: Verificar la instalación
echo "Verificando la instalación de OMNeT++..."
cd samples/aloha
./aloha

# Paso 6: Crear accesos directos de escritorio
echo "Creando accesos directos de escritorio..."
cd $INSTALL_DIR/omnetpp-6.0
make install-menu-item
make install-desktop-icon

# Paso 7: Instalar paquetes requeridos
echo "Instalando paquetes requeridos..."
sudo apt-get update
sudo apt-get install build-essential clang lld gdb bison flex perl \
python3 python3-pip qtbase5-dev qtchooser qt5-qmake qtbase5-dev-tools \
libqt5opengl5-dev libxml2-dev zlib1g-dev doxygen graphviz libwebkit2gtk-4.0-37
python3 -m pip install --user --upgrade numpy pandas matplotlib scipy seaborn posix_ipc
sudo apt-get install openscenegraph-plugin-osgearth libosgearth-dev
sudo apt-get install libopenscenegraph-dev
sudo apt-get install mpi-default-dev

# Paso 8: Descargar y descomprimir INET, Simu5G y Veins
echo "Descargando INET..."
wget $INET_URL -O $INET_FILE

echo "Descargando Simu5G..."
wget $SIMU5G_URL -O $SIMU5G_FILE

echo "Descargando Veins..."
wget $VEINS_URL -O $VEINS_FILE

echo "Ejecute OMNeT"