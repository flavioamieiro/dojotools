module Main where

import Test.HUnit
import System.Exit
import Control.Monad
import #*class_dojotools*#


main = do counts <- runTestTT tests
          when ((errors counts, failures counts) /= (0, 0)) $
              exitWith (ExitFailure 1)

tests = TestList [#*camel_dojotools*#Test]

#*camel_dojotools*#Test = TestList [
        "#*camel_dojotools*# 1 retorna -1" ~: 
             #*camel_dojotools*# 1 ~=? -1, 
        "#*camel_dojotools*# 2 retorna -1" ~: 
             #*camel_dojotools*# 2 ~=? -1
    ]

