#!/usr/bin/env sh

export PORT=8000

#
# starting the server
#
cms analytics codegen sklearn linearmodel --service=LinearRegression --port=$PORT --dir=./build --host=127.0.0.1
cms analytics server start  --cloud=local --service=LinearRegression --dir=./build --detached

# --detached
#sleep 3

#
# NOT SURE WHAT THIS DOES
#
# cms analytics LinearRegression --port=$PORT


#
# Testing FILE functions
#
# touch build/LinearRegression/data/test.csv
# cms analytics file upload LinearRegression tests/data/user_input_data.csv
# cms analytics file list LinearRegression

#
# Help
#
# cms analytics help sklearn.linear_model.LinearRegression
# cms analytics manual LinearRegression


#
# TODO
#

##cms analytics LinearRegression fit X="[[1,2]]" y="[[3,4]]" --port=$PORT
##cms analytics LinearRegression predict X="[[1,2]]"
#
##cms analytics LinearRegression predict X=user_input_data
#
##cms analytics file read filename=user_input_data



#ok# cms analytics server stop LinearRegression
