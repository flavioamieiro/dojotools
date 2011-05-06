#include "simplectest/tests.h"
#include "#*down_dojotools*#.c"

START_TESTS()

START_TEST("Testar #*class_dojotools*#")

    TEST("#*dojotools*# deve retornar 1");
    ASSERT(#*dojotools*#() == 1);
//    ASSERT_EQUALS_FLOAT(1, 1);

END_TEST()


END_TESTS()
