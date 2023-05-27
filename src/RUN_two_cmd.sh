#!/bin/bash
nohup socat TCP4-LISTEN:5001,reuseaddr,fork TCP:host.docker.internal:5432 & 
flask run --host=0.0.0.0 