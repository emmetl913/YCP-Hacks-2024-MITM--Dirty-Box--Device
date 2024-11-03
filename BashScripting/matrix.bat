@Echo Off & CD "%~dp0"

:: Set console dimensions
Set "Console_Height=5"
Set "Console_Width=170"

:: Set color variables
Setlocal EnableDelayedExpansion
Set /A Red=31, Green=32, Yellow=33, Blue=34, Purple=35, Cyan=36, White=37, Off=0
For %%A in (Red, Green, Yellow, Blue, Purple, Cyan, White, Off) do (
    Set "%%A=[!%%A!m"
)

:main
:: Set console properties
@Mode Con: lines=%Console_Height% cols=%Console_Width%
@Title Flow Matrix

:1loop
:: Infinite loop for the flow matrix effect
For /L %%A in (1,1,125) do (
    Set /A Xpos=!random! %%!Console_Width! + 1, Ypos=!random! %%!Console_Height! + 1, Char=!random! %%80 + 1
    Echo(![!Ypos!]!!Xpos! C!Char! !Green!
)
Goto :1loop
