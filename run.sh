#!/bin/bash

function init {
    # Create log directory
    mkdir -p log
}

function run_services {
    # Library registration service
    python3 worker.py 8001 1 1>log/library.out 2>log/library.err &
    if [ $! -eq 0 ]; then
        library_pid=$!
        echo Library registration service is up.
    else
        echo Library registration service failed to run!
    fi

    # Dormitory registration service
    python3 worker.py 8002 2 1>log/dorm.out 2>log/dorm.err &
    if [ $! -eq 0 ]; then
        dorm_pid=$!
        echo Dormitory registration service is up.
    else
        echo Dormitory registration service failed to run!
    fi

    # Pool registration service
    python3 worker.py 8003 3 1>log/pool.out 2>log/pool.err &
    if [ $! -eq 0 ]; then
        pool_pid=$!
        echo Pool registration service is up.
    else
        echo Pool registration service failed to run!
    fi

    # The load balancer
    python3 load-balancer.py 1>log/load-balancer.out 2>log/load-balancer.err &
    if [ $! -eq 0 ]; then
        load_balancer_pid=$!
        echo Load balancer is up.
    else
        echo Load balancer failed to run!
    fi
}

function run_client {
    echo Enter your commands:
    python3 client.py
}

function shutdown {
    echo $library_pid $dorm_pid $pool_pid $load_balancer_pid
    kill -SIGINT $library_pid $dorm_pid $pool_pid $load_balancer_pid
    if [ $! -eq 0 ]; then
        echo Shutdown successfuly!
    else
        echo Shutdown failed!
    fi
}

function main {
    init
    run_services
    run_client
}

# The execution start point
trap shutdown SIGINT
main
