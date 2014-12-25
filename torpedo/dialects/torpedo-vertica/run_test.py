__author__ = 'kbroughton'

from sqlalchemy.dialects import registry

registry.register("vertica", "torpedo_vertica.pyodbc", "Vertica_pyodbc")
registry.register("vertica.pyodbc", "torpedo_vertica.pyodbc", "Vertica_pyodbc")

from torpedo.testing import runner

# use this in setup.py 'test_suite':
# test_suite="run_tests.setup_py_test"
def setup_py_test():
    runner.setup_py_test()

if __name__ == '__main__':
    runner.main()