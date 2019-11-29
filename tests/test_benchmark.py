"""
Generate benchmarks for endpoint functions
"""
import subprocess
import numpy as np
from cloudmesh.common.StopWatch import StopWatch


class TestBenchmark:
    @pytest.fixture
    def generated_data_file(self):
        xs = np.random()
        ys = 3*xs + 1 + np.random()
        data_file = write(xs, ys)
        return data_file

    def test_file_upload_benchmark(self, generated_data_file):
        StopWatch.start()
        subprocess.call(['cms', 'analytics', ...])
        StopWatch.stop()

    def test_list_file_benchmark(self):
        StopWatch.start()
        subprocess.call(['cms', 'analytics', ])
        StopWatch.stop()

    def test_read_file_benchmark(self, generated_data_file):
        StopWatch.start()
        subprocess.call(['cms', 'analytics', ])
        StopWatch.stop()

    def test_linear_consturctor_benchmark(self):
        StopWatch.start()
        subprocess.call(['cms', 'analytics', 'LinearRegression'])
        StopWatch.stop()

    def test_linear_fit_benchmark(self):
        StopWatch.start()
        subprocess.call(['cms', 'analytics', 'LinearRegression', 'fit'])
        StopWatch.stop()

    def test_linear_get_params_benchmark(self):
        StopWatch.start()
        subprocess.call(['cms', 'analytics', 'LinearRegression', 'get_params'])
        StopWatch.stop()

    def test_linear_predict_benchmark(self):
        StopWatch.start()
        subprocess.call(['cms', 'analytics', 'LinearRegression', 'predict'])
        StopWatch.stop()

    def test_linear_score_benchmark(self):
        StopWatch.start()
        subprocess.call(['cms', 'analytics', 'LinearRegression', 'score'])
        StopWatch.stop()

    def test_print_benchmark(self):
        StopWatch.benchmark()
        StopWatch.clear()
        assert 1==0
