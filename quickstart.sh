#!/usr/bin/env sh

export PORT=8000

cms analytics codegen sklearn linearmodel --service=LinearRegression --port=$PORT --dir=./build --host=127.0.0.1
cms analytics server start  --cloud=local --service=LinearRegression --dir=./build

# touch build/LinearRegression/data/a.csv
# cms analytics file list LinearRegression

cms analytics file upload LinearRegression tests/test_uploaded_files/user_input_data.csv

# --detached
#sleep 3

# ok #cms analytics LinearRegression --port=$PORT


##cms analytics LinearRegression fit X="[[1,2]]" y="[[3,4]]" --port=$PORT
##cms analytics LinearRegression predict X="[[1,2]]"
#
##cms analytics LinearRegression predict X=user_input_data
#
#cms analytics file read filename=user_input_data
#cms analytics server stop

