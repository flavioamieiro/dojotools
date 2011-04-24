module Main where

import Test.HUnit
import System.Exit
import Control.Monad
import #*up_dojotools*#


main = do counts <- runTestTT tests
          when ((errors counts, failures counts) /= (0, 0)) $
              exitWith (ExitFailure 1)

tests = TestList [#*dojotools*#Test]

#*dojotools*#Test = TestList [
        "#*dojotools*# 1 retorna -1" ~: 
             #*dojotools*# 1 ~=? -1, 
        "#*dojotools*# 2 retorna -1" ~: 
             #*dojotools*# 2 ~=? -1
    ]

