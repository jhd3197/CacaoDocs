import unittest
import sys
from tests.package_test import TestPackage
from tests.types_test import TestTypes
from tests.flask_test import TestAPIEndpoints

def get_test_suite(test_names=None):
    test_classes = {
        'package': TestPackage,
        'types': TestTypes,
        'flask': TestAPIEndpoints,
        'all': [TestPackage, TestTypes, TestAPIEndpoints]
    }
    
    suite = unittest.TestSuite()
    
    if not test_names:
        test_names = ['all']
        
    for name in test_names:
        if name.lower() in test_classes:
            if isinstance(test_classes[name.lower()], list):
                for test_class in test_classes[name.lower()]:
                    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(test_class))
            else:
                suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(test_classes[name.lower()]))
    
    return suite

if __name__ == "__main__":
    test_names = sys.argv[1:] if len(sys.argv) > 1 else None
    runner = unittest.TextTestRunner()
    runner.run(get_test_suite(test_names))
