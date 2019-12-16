#!/usr/bin/env sh

cd ../build/
docker build -t LinearRegression .
docker run -p 5000:5000 -d LinearRegression
cd ../command/