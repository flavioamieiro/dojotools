module Main where

import Test.HUnit
import System.Exit
import Control.Monad
import #_#class_dojotools#_#


main = do counts <- runTestTT tests
          when ((errors counts, failures counts) /= (0, 0)) $
              exitWith (ExitFailure 1)

tests = TestList [#_#camel_dojotools#_#Test]

#_#camel_dojotools#_#Test = TestList [
        "#_#camel_dojotools#_# 1 retorna -1" ~: 
             #_#camel_dojotools#_# 1 ~=? -1, 
        "#_#camel_dojotools#_# 2 retorna -1" ~: 
             #_#camel_dojotools#_# 2 ~=? -1
    ]

