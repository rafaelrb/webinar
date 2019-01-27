#!/bin/bash

kubeadm token list | tail -1 | awk '{print $1}'
