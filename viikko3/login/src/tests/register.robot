*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application Create User And Go To Register Page

*** Test Cases ***
Register With Valid Username And Password
    Set Username  uus
    Set Password  uusi1234
    Set Password Confirmation  uusi1234
    Click  button >> text=Register
    Register Should Succeed

Register With Too Short Username And Valid Password
    Set Username  ab
    Set Password  uusi1234
    Set Password Confirmation  uusi1234
    Click  button >> text=Register
    Register Should Fail With Message  Username must be at least 3 characters long

Register With Valid Username And Too Short Password
    Set Username  uus
    Set Password  uusi123
    Set Password Confirmation  uusi123
    Click  button >> text=Register
    Register Should Fail With Message  Password must be at least 8 characters long

Register With Username That Is Already In Use
    Set Username  kalle
    Set Password  uusi1234
    Set Password Confirmation  uusi1234
    Click  button >> text=Register
    Register Should Fail With Message  Username is already in use

*** Keywords ***
Set Password Confirmation
    [Arguments]  ${password}
    Fill Secret  id=password_confirmation  $password

Register Should Succeed
    Get Url  ==  http://${SERVER}/welcome

Register Should Fail With Message
    [Arguments]  ${message}
    Register Page Should Be Open
    Get Text  body  *=  ${message}

Reset Application Create User And Go To Register Page
    Reset Application
    Create User  kalle  kalle1234
    Go To Register Page
