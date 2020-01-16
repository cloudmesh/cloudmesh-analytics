#!/usr/bin/env sh

banner()
{
	echo
	echo "############################################################"
	echo "# $1 "
	echo "############################################################"
}

export PORT=8000

#
# starting the server
#
banner "START THE SERVER"

cms analytics codegen sklearn linearmodel --service=LinearRegression --port=$PORT --dir=./build --host=127.0.0.1
cms analytics server start  --cloud=local --service=LinearRegression --dir=./build --detached

sleep 3

banner "INITIALIZE THE SERVER"

cms analytics LinearRegression --port=$PORT


#
# Testing FILE functions
#
touch build/LinearRegression/data/test.csv

banner "UPLOAD A FILE"

cms analytics file put LinearRegression tests/data/user_input_data.csv

banner "LIST THE FILE"
cms analytics file list LinearRegression

banner "GET THE FILE"
cms analytics file get LinearRegression user_input_data.csv

#
# Help
#
banner "HELP ON SKLEARN"

echo |  cms analytics help sklearn.linear_model.LinearRegression

banner "MANUAL PAGE TO INTERACT WITH THE SERVICE"

cms analytics manual LinearRegression


banner "DO A FIT"

cms analytics run LinearRegression fit X="[[1,2]]" y="[[3,4]]" --port=$PORT

banner "DO A PREDICT"

cms analytics run LinearRegression predict X="[[1,2]]" --port=$PORT

##cms analytics LinearRegression predict X=user_input_data
# analytics file run SERVICE PARAMETERS... FILENAME [--cloud=CLOUD] [--port=PORT] [-v]

$(call banner, "STOP THE SERVER")

cms analytics server stop LinearRegression
