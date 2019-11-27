"""
Generate benchmarks for endpoint functions
"""

from cloudmesh.common.StopWatch import StopWatch

class TestBenchmark:
    @pytest.fixture
    def generated_data_file(self):
        pass

    def test_file_upload_benchmark(self, generated_data_file):
        pass

    def test_list_file_benchmark(self):
        pass

    def test_read_file_benchmark(self, filename):
        pass

    def test_linear_consturctor_benchmark(self):
        pass

    def test_linear_fit_benchmark(self):
        pass

    def test_linear_get_params_benchmark(self):
        pass

    def test_linear_predict_benchmark(self):
        pass

    def test_linear_score_benchmark(self):
        pass

    def test_print_benchmark(self):
        pass
