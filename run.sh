#!/bin/bash

__docker_exe="docker"
__compose_exe="docker compose"

__command="$1"
shift

up() {
    ${__compose_exe} -f node.yml -f web3signer.yml up -d --remove-orphans
}

down() {
    ${__compose_exe} -f node.yml -f web3signer.yml down --remove-orphans
}

build() {
    ${__compose_exe} -f node.yml -f web3signer.yml build
}

logs() {
    ${__docker_exe} container logs "$@"
}

case "$__command" in
    up)
        up
        ;;
    down)
        down
        ;;
    build)
        build
        ;;
    logs)
        logs "$@"
        ;;
    *)
        echo "Usage: $0 {up|down|build}"
        exit 1
esac