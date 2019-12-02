"""
Generate benchmarks for endpoint functions
"""
import pytest, subprocess, os
import numpy as np
from cloudmesh.common.StopWatch import StopWatch


class TestBenchmark:
    @pytest.fixture
    def test_project_uploaded_file_path(self):
        return os.path.join(os.path.dirname(__file__), "test_uploaded_files")

    def test_generated_data_file(self, test_project_uploaded_file_path):
        xs = np.random.rand(50, 2)
        ys = np.dot(xs, np.random.rand(2, 1)) + np.random.rand(50, 1)

        np.savetxt(os.path.join(test_project_uploaded_file_path, "user_input_data.csv"), np.asarray(xs), delimiter=",")
        np.savetxt(os.path.join(test_project_uploaded_file_path, "user_output_data.csv"), np.asarray(ys), delimiter=",")

        assert 1 == 1

    def test_file_upload_benchmark(self, test_project_uploaded_file_path):
        StopWatch.start("File_upload")
        subprocess.call(['cms', 'analytics', 'file', 'upload', '--filename=user_input_data.csv'])
        subprocess.call(['cms', 'analytics', 'file', 'upload', '--filename=user_output_data.csv'])
        StopWatch.stop("File_upload")
        assert 1 == 1


    def test_list_file_benchmark(self):
        StopWatch.start("File_list")
        subprocess.call(['cms', 'analytics', 'file', 'list'])
        StopWatch.stop("File_list")
        assert 1 == 1

    def test_read_file_benchmark(self):
        StopWatch.start("File_read")
        subprocess.call(['cms', 'analytics', 'file', 'read', '--filename=user_input_data'])
        subprocess.call(['cms', 'analytics', 'file', 'read', '--filename=user_output_data'])
        StopWatch.stop("File_read")
        assert 1 == 1

    def test_linear_consturctor_benchmark(self):
        StopWatch.start('LinearRegression_constructor')
        subprocess.call(['cms', 'analytics', 'LinearRegression', '--fit_intercept=true', '--normalize=false'])
        StopWatch.stop('LinearRegression_constructor')
        assert 1 == 1

    def test_linear_fit_benchmark(self):
        StopWatch.start("LinearRegression_fit")
        subprocess.call(['cms', 'analytics', 'LinearRegression', 'fit', '--X=user_input_data', '-y=user_output_data'])
        StopWatch.stop("LinearRegression_fit")
        assert 1 == 1

    def test_linear_get_params_benchmark(self):
        StopWatch.start("LinearRegression_get_params")
        subprocess.call(['cms', 'analytics', 'LinearRegression', 'get_params'])
        StopWatch.stop("LinearRegression_get_params")

    def test_linear_predict_benchmark(self):
        StopWatch.start("LinearRegression_predict")
        subprocess.call(['cms', 'analytics', 'LinearRegression', 'predict', '--X=[[0,0],[0,1],[0,2]]'])
        StopWatch.stop("LinearRegression_predict")
        assert 1 == 1

    def test_linear_score_benchmark(self):
        StopWatch.start("LinearRegression_score")
        subprocess.call(['cms', 'analytics', 'LinearRegression', 'score', '--X=user_input_data', '--y=user_output_data'])
        StopWatch.stop("LinearRegression_score")
        assert 1 == 1

    def test_linear_property_benchmark(self):
        StopWatch.start("LinearRegression_get_property")
        subprocess.call(['cms', 'analytics', 'LinearRegression', 'get_property'])
        StopWatch.stop("LinearRegression_get_property")
        assert 1 == 1

    def test_print_benchmark(self):
        StopWatch.benchmark()
        StopWatch.clear()
        assert 1 == 0
