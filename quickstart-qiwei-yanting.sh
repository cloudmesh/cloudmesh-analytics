# generate code for two services
$ cms analytics codegen sklearn linearmodel --class_name=LinearRegression --port=5000
$ cms analytics codegen sklearn linearmodel --class_name=LogisticRegression --port=5001
 
# start the two services
$ cms analytics server start --cloud=local --class_name=LinearRegression
$ cms analytics server start --cloud=local --class_name=LogisticRegression
 
# upload files in two servers (Assuming terminal is in PATH/cloudmesh-analytics/)
$ cd ./tests/test_uploaded_files/ 
$ cms analytics --class_name=LinearRegression file upload --filename=user_input_data.csv
$ cms analytics --class_name=LogisticRegression file upload --filename=user_output_data.csv

# list the files in two servers
$ cms analytics --class_name=LinearRegression file list
$ cms analytics --class_name=LogisticRegression file list

# read the uploaded files in two servers
$ cms analytics  --class_name=LinearRegression file read --filename=user_input_data
$ cms analytics  --class_name=LogisticRegression file read --filename=user_output_data

# run the functionality of LinearRegression server
$ cms analytics cons --class_name=LinearRegression
$ cms analytics --class_name=LinearRegression fit --X=[[1,2],[3,4]] --y=[5,6]
$ cms analytics --class_name=LinearRegression predict --X=[[3,4]]
$ cms analytics --class_name=LinearRegression get_params

# run the functionality of LogisticRegression server
$ cms analytics cons --class_name=LogisticRegression
$ cms analytics --class_name=LogisticRegression fit --X=[[1,2],[3,4]] --y=[0,1]
$ cms analytics --class_name=LogisticRegression predict --X=[[3,4]]
$ cms analytics --class_name=LogisticRegression get_params

# stop the two services
$ cms analytics server stop --cloud=local --class_name=LinearRegression
$ cms analytics server stop --cloud=local --class_name=LogisticRegression
