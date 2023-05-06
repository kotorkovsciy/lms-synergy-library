import doctest
import sys
sys.path.append('../')
import lms_synergy_library

result: doctest.TestResults = doctest.testmod(lms_synergy_library.lms_synergy_library)

if result.failed == 0:
    print("ALL TESTS PASSED")
else:
    print("FAILED TESTS: ", result.failed)
