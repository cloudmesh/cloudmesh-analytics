"""
Generate benchmarks for endpoint functions
"""
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

        StopWatch.stop()
        pass

    def test_list_file_benchmark(self):
        StopWatch.start()
        StopWatch.stop()
        pass

    def test_read_file_benchmark(self, filename):
        StopWatch.start()
        StopWatch.stop()
        pass

    def test_linear_consturctor_benchmark(self):
        StopWatch.start()
        StopWatch.stop()
        pass

    def test_linear_fit_benchmark(self):
        StopWatch.start()
        StopWatch.stop()
        pass

    def test_linear_get_params_benchmark(self):
        StopWatch.start()
        StopWatch.stop()
        pass

    def test_linear_predict_benchmark(self):
        StopWatch.start()
        StopWatch.stop()
        pass

    def test_linear_score_benchmark(self):
        StopWatch.start()
        StopWatch.stop()
        pass

    def test_print_benchmark(self):
        StopWatch.benchmark()
        pass
