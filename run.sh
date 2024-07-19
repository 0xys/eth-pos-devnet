#!/bin/bash

__docker_exe="docker"
__compose_exe="docker compose"

up() {
    ${__compose_exe} -f node.yml -f web3signer.yml up -d
}

down() {
    ${__compose_exe} -f node.yml -f web3signer.yml down
}

build() {
    ${__compose_exe} -f node.yml -f web3signer.yml build
}

case "$1" in
    up)
        up
        ;;
    down)
        down
        ;;
    build)
        build
        ;;
    *)
        echo "Usage: $0 {up|down|build}"
        exit 1
esac