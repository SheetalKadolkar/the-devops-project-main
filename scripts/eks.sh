#!/bin/bash
# Basic EKS Cluster Creation Script
# Author: Atul Kamble

eksctl create cluster \
  --name my-eks-cluster \
  --region us-east-1 \
  --node-type t3.small \
  --nodes 2 \
  --nodes-min 2 \
  --nodes-max 2 \
  --managed
