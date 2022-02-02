#!/bin/sh

export $(cat .env.example | xargs)
export $(cat .env | xargs)

python3 src '$@'