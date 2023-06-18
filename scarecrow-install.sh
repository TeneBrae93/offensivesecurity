#!/bin/bash

sudo apt-get install golang

go get github.com/fatih/color
go get github.com/yeka/zip
go get github.com/josephspurrier/goversioninfo

sudo apt-get install osslsigncode
sudo apt-get install mingw-w64

mkdir bypass
cd bypass
git clone https://github.com/optiv/ScareCrow
cd ScareCrow
go build ScareCrow.go
./ScareCrow 
