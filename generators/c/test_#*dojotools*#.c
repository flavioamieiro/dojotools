#include "simplectest/tests.h"
#include "#*dojotools*#.c"

START_TESTS()

START_TEST("Testar #*up_dojotools*#")

    TEST("#*up_dojotools*# deve retornar 1");
    ASSERT(#*dojotools*#() == 1);
//    ASSERT_EQUALS_FLOAT(1, 1);

END_TEST()


END_TESTS()
