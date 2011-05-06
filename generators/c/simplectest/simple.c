/*
 * This demonstrates the simplest way to do some tests using simplectest.
 * See "readme.txt" for more information, or the website at
 * http://simplectest.sf.net/.
 *
 * Jevon Wright 2004-05
 */
#include "tests.h"

// Start the overall test suite
START_TESTS()

// A new group of tests, with an identifier
START_TEST("simple")
	// We then write the tests we want to check
	ASSERT(1 == 1);
	ASSERT_EQUALS_FLOAT(1, 1);
END_TEST()

START_TEST("fail")
	// These tests will fail, and we will get output.
	ASSERT(1 == 0);
	ASSERT_EQUALS_FLOAT(1, 0);

	// Lets give a description of the test, before it
	// fails - this will be printed out instead.
	TEST("we expect this test to fail. (3==2)");
	ASSERT(3 == 2);
END_TEST()

// End the overall test suite
END_TESTS()
