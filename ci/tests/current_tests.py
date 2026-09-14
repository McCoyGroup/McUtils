import sys

TEST_MODULE = 'ClaudeCombinatoricsTests'
sys.argv.extend(['-f', TEST_MODULE])

from run_tests import run_tests
run_tests()