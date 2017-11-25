#!/bin/bash

kubectl create -f k8s/deploy-frontend.yml

kubectl expose deployment frontend --type=NodePort

kubectl apply -f k8s/basic-ingress.yml

