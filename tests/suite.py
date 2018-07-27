import unittest

from create import CreateTodoTest
from modify import ModifyTodoTest
from clear import ClearTodoTest

create = unittest.TestLoader().loadTestsFromTestCase(CreateTodoTest)
modify = unittest.TestLoader().loadTestsFromTestCase(ModifyTodoTest)
clear = unittest.TestLoader().loadTestsFromTestCase(ClearTodoTest)

test_suite = unittest.TestSuite([create, modify, clear])

# run the suite
unittest.TextTestRunner(verbosity=3).run(test_suite)