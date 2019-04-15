from deicode.scripts._standalone_rpca import standalone_rpca
import unittest
import pandas as pd
from os.path import sep as os_path_sep
from click.testing import CliRunner
from skbio import OrdinationResults
from skbio.util import get_data_path
from numpy.testing import assert_array_almost_equal
from deicode.testing import assert_deicode_ordinationresults_equal


class Test_standalone_rpca(unittest.TestCase):
    def setUp(self):
        pass

    def test_standalone_rpca(self):
        """Checks the output produced by DEICODE's standalone script.

           This is more of an "integration test" than a unit test -- the
           details of the algorithm used by the standalone RPCA script are
           checked in more detail in deicode/tests/test_optspace.py, etc.
        """
        in_ = get_data_path('test.biom')
        out_ = os_path_sep.join(in_.split(os_path_sep)[:-1])
        runner = CliRunner()
        result = runner.invoke(standalone_rpca, ['--in-biom', in_,
                                                 '--output-dir', out_])
        # Read the results
        dist_res = pd.read_csv(get_data_path('distance-matrix.tsv'), sep='\t',
                               index_col=0)
        ord_res = OrdinationResults.read(get_data_path('ordination.txt'))

        # Read the expected results
        dist_exp = pd.read_csv(get_data_path('expected-distance-matrix.tsv'),
                               sep='\t', index_col=0)
        ord_exp = OrdinationResults.read(get_data_path(
                                         'expected-ordination.txt'))

        # Check that the distance matrix matches our expectations
        assert_array_almost_equal(dist_res.values, dist_exp.values)

        # Check that the ordination results match our expectations -- checking
        # each value for both features and samples
        assert_deicode_ordinationresults_equal(ord_res, ord_exp)

        # Lastly, check that DEICODE's exit code was 0 (indicating success)
        self.assertEqual(result.exit_code, 0)


if __name__ == "__main__":
    unittest.main()