#!/usr/bin/env sh


cms analytics codegen sklearn linearmodel --service=LinearRegression --port=8000 --dir=./build --host=127.0.0.1


#cms analytics codegen sklearn linearmodel --class_name=LinearRegression --port=8000
#@cms analytics server start detached --cloud=local --class_name=LinearRegression --port=8000
#sleep 3

#cms analytics LinearRegression
##cms analytics LinearRegression fit X="[[1,2]]" y="[[3,4]]"
##cms analytics LinearRegression predict X="[[1,2]]"
#cms analytics file upload filename=tests/test_uploaded_files/user_input_data.csv
##cms analytics LinearRegression predict X=user_input_data
#cms analytics file list
#cms analytics file read filename=user_input_data
#cms analytics server stop

