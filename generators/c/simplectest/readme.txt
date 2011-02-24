simplectest 0.31: A Simple C++ Testing Framework
Copyright (c) 2005 Jevon Wright
http://simplectest.sourceforge.net


This package is a simple testing framework for C and C++.

I wrote this framework when I got fed up with the flaws in other testing 
frameworks for C or C++. Because C++ is strictly typed and doesn't have support
for reflection, all other resting frameworks:
- Required that you write out the test function names more than once; or
- Required that you use a scripting language to generate the list of tests.

Inspired by an article on C2.com, I wrote this - a simple, but very effective
testing framework for C and C++. It is based on macros. It is not as full-
featured as other testing frameworks, but it gets the job done and lets you
focus on writing tests (and making them pass).

This project was developed as a side project to a summer project at
Massey University over 2004/2005.


1. How to install
2. Features
3. How to use
4. Suites
5. Bugs and comments


------------------------------------------------------------------------
1. HOW TO INSTALL

No make/configure is required. All you need to do is include the macro
definitions in your test files:
	#include "simplectest/tests.h"

See "How to use" for more information, and tips on how to get started.
Also check the website for tips and tricks on how to use this framework
more effectively.


------------------------------------------------------------------------
2. FEATURES

- You only have to write each test once. In other testing frameworks, 
  you have to write test function names more than once (because C++ 
  does not have reflection).
  
- You don't need to deal with Autoconf or Make if you don't want to. 
  It's up to you if you want to automate testing (highly recommended).

- You don't need to use a scripting language like Perl to generate the 
  lists of tests to run.
  
- You don't need to try and dance with complex features like templates.

- It can run in both C and C++.

- It's very simple. If you need to extend the framework, it's easy to 
  adjust it. You don't need to configure a million things just to get 
  some tests running.
  
- It's portable.

- It's free and open source. Yay ^_^


------------------------------------------------------------------------
3. HOW TO USE

"simplectest" is designed to be used at the same time as implementation 
of your application. It provides a simple framework for running code, 
checking assertions and producing a report at the end.

The library does not have to be included in your final application, and 
all testing can be completely independent of your actual code.

See "simple.c" for an example of a testing file. Once you have compiled
and linked it, you will get output similar to:

	$ ./simple
	> simple...
	> fail...
	[FAIL] simple.c:21 : (fail) : 1 == 0 fails
	[FAIL] simple.c:22 : (fail) : 1 is supposed to equal (float) 0
		(0.000000 != 1.000000)
	[FAIL] simple.c:26 : (fail) : we expect this test to fail. (3==2)

	--- Results ---
	Tests run:    2
	Passes:       2
	Failures:     3


------------------------------------------------------------------------
4. SUITES

 A Test Suite is a composite used to group similar tests together, 
 allowing you to test them as a group (instead of individually). 
 simplectest has limited support for the concept of testing suites.

To write a test suite, first put the test suite into its own file:

[test-suite.cpp]
	#include "test-suite.h"

	START_SUITE(mysuite)

	START_TEST("myTest")
	   ... normal testing code ...
	END_TEST()

	... more tests ...

	END_SUITE()

Make a header file for the test suite:

[test-suite.h]
	#ifndef _TESTS_SUITE_H
	#define _TESTS_SUITE_H

	// include test definitions
	#include "simplectest/tests.h"

	// create suite declaration
	DEFINE_SUITE(mysuite)

	#endif

Finally, in the actual test file, add the suite header declaration and 
the call to run the suite:

[tests.cpp]
	#include "simplectest/tests.h"
	#include "test-suite.h"

	START_TESTS()

	// run mysuite
	SUITE(mysuite);

	END_TESTS()

That's all you need to do. You can then compile all the source code, 
link the classes together, and voila - a test suite. To disable the 
test suite, you can simply comment out the SUITE() line in the main 
test file.

You can run the suite individually by defining 'TEST_INDIVIDUAL' when
compiling the suite, i.e.
	$ g++ test-suite.cpp -o test-suite.o -DTEST_INDIVIDUAL
	$ g++ test-suite.o -o test-suite
	$ ./test-suite


------------------------------------------------------------------------
5. BUGS AND COMMENTS

If you have any bugs, problems, comments or suggestions, they would be well
appreciated. Please use the tools available at the website:
	http://simplectest.sourceforge.net

Alternatively, contact the author via e-mail:
	support@jevon.org
