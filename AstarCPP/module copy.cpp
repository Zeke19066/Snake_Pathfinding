#include <pybind11/pybind11.h>
#include <windows.h>
#include <stdio.h>      /* printf, scanf, puts, NULL */
#include <stdlib.h>     /* srand, rand */
#include <time.h>       /* time */
#include <iostream>

using namespace std;

void actionMapMinmap(int action, int lastAction)
{
    int moveKeys[5] = {0x11, 0x10, 0x1f, 0x1e, 0x20}; //WQSAD keys

    if (lastAction == action)
    {
        return;
    }

    else if (lastAction != action)
    {

        // This structure will be used to create the keyboard
        // input event.
        INPUT ipAct; // Set up a generic keyboard event.
        ipAct.type = INPUT_KEYBOARD;
        ipAct.ki.wVk = 0; //We're doing scan codes instead
        ipAct.ki.time = 0;
        ipAct.ki.dwExtraInfo = 0;

        //First remove lastAction
        ipAct.ki.wScan = moveKeys[lastAction]; //Select last key
        ipAct.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP;
        SendInput(1, &ipAct, sizeof(INPUT));

        //Start with a W
        ipAct.ki.wScan = moveKeys[0]; //Select W
        ipAct.ki.dwFlags = KEYEVENTF_SCANCODE;
        SendInput(1, &ipAct, sizeof(INPUT));

        if (action == 0)//Forward
        {
            return;
        }
        if (action == 1)//Power-Up
        {
            ipAct.ki.wScan = moveKeys[1]; //Select Q
            ipAct.ki.dwFlags = KEYEVENTF_SCANCODE;
            SendInput(1, &ipAct, sizeof(INPUT));
            return;
        }
        if (action == 2)//Reverse
        {   //first remove the W
            ipAct.ki.wScan = moveKeys[0]; //Select W
            ipAct.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP;
            SendInput(1, &ipAct, sizeof(INPUT));

            //Then press down S
            ipAct.ki.wScan = moveKeys[2]; //Select S
            ipAct.ki.dwFlags = KEYEVENTF_SCANCODE;
            SendInput(1, &ipAct, sizeof(INPUT));
            return;
        }
        if (action == 3)//Left
        {
            ipAct.ki.wScan = moveKeys[3]; //Select A
            ipAct.ki.dwFlags = KEYEVENTF_SCANCODE;
            SendInput(1, &ipAct, sizeof(INPUT));
            return;
        }
        if (action == 4)//Right
        {
            ipAct.ki.wScan = moveKeys[4]; //Select D
            ipAct.ki.dwFlags = KEYEVENTF_SCANCODE;
            SendInput(1, &ipAct, sizeof(INPUT));
            return;
        }
        return;
    }
};

void actionMapSpeed(int action, int lastAction)
{
    int moveKeys[5] = {0x11, 0x10, 0x1f, 0x1e, 0x20}; //WQSAD keys

    // This structure will be used to create the keyboard
    // input event.
    INPUT ipAct; // Set up a generic keyboard event.
    ipAct.type = INPUT_KEYBOARD;
    ipAct.ki.wVk = 0; //We're doing scan codes instead
    ipAct.ki.time = 0;
    ipAct.ki.dwExtraInfo = 0;

    //First remove lastAction
    ipAct.ki.wScan = moveKeys[lastAction]; //Select last key
    ipAct.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP;
    SendInput(1, &ipAct, sizeof(INPUT));

    //Start with a W
    ipAct.ki.wScan = moveKeys[0]; //Select W
    ipAct.ki.dwFlags = KEYEVENTF_SCANCODE;
    SendInput(1, &ipAct, sizeof(INPUT));

    if (action == 0)//Forward
    {
        return;
    }
    if (action == 1)//Power-Up
    {
        //first remove the W
        //ipAct.ki.wScan = moveKeys[0]; //Select W
        //ipAct.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP;
        //SendInput(1, &ipAct, sizeof(INPUT));

        //Then fire power-up
        ipAct.ki.wScan = moveKeys[1]; //Select Q
        ipAct.ki.dwFlags = KEYEVENTF_SCANCODE;
        SendInput(1, &ipAct, sizeof(INPUT));
        return;
    }
    if (action == 2)//Reverse
    {   //first remove the W
        ipAct.ki.wScan = moveKeys[0]; //Select W
        ipAct.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP;
        SendInput(1, &ipAct, sizeof(INPUT));

        //Then press down S
        ipAct.ki.wScan = moveKeys[2]; //Select S
        ipAct.ki.dwFlags = KEYEVENTF_SCANCODE;
        SendInput(1, &ipAct, sizeof(INPUT));
        return;
    }
    if (action == 3)//Left
    {
        ipAct.ki.wScan = moveKeys[3]; //Select A
        ipAct.ki.dwFlags = KEYEVENTF_SCANCODE;
        SendInput(1, &ipAct, sizeof(INPUT));
        return;
    }
    if (action == 4)//Right
    {
        ipAct.ki.wScan = moveKeys[4]; //Select D
        ipAct.ki.dwFlags = KEYEVENTF_SCANCODE;
        SendInput(1, &ipAct, sizeof(INPUT));
        return;
    }
    return;
    
};

void actionMapMinmapDrift(int action, int lastAction)
{
    int moveKeys[6] = {0x11, 0x10, 0x1f, 0x1e, 0x20, 0x12}; //WQSADE keys

    if (lastAction == action)
    {
        return;
    }

    else if (lastAction != action)
    {

        // This structure will be used to create the keyboard
        // input event.
        INPUT ipAct; // Set up a generic keyboard event.
        ipAct.type = INPUT_KEYBOARD;
        ipAct.ki.wVk = 0; //We're doing scan codes instead
        ipAct.ki.time = 0;
        ipAct.ki.dwExtraInfo = 0;

        //First remove lastAction
        ipAct.ki.wScan = moveKeys[lastAction]; //Select last key
        ipAct.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP;
        SendInput(1, &ipAct, sizeof(INPUT));

        if ((lastAction == 2)||(lastAction == 3)) //OR conditional for removing power slide
        {   
            ipAct.ki.wScan = moveKeys[5];//Select powerslide
            ipAct.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP;
            SendInput(1, &ipAct, sizeof(INPUT));
        }

        //Start with a W
        ipAct.ki.wScan = moveKeys[0]; //Select W
        ipAct.ki.dwFlags = KEYEVENTF_SCANCODE;
        SendInput(1, &ipAct, sizeof(INPUT));

        if (action == 0)//Forward
        {
            return;
        }
        if (action == 1)//Power-Up
        {
            ipAct.ki.wScan = moveKeys[1]; //Select Q
            ipAct.ki.dwFlags = KEYEVENTF_SCANCODE;
            SendInput(1, &ipAct, sizeof(INPUT));
            return;
        }
        if (action == 2)//Reverse
        {   //first remove the W
            ipAct.ki.wScan = moveKeys[0]; //Select W
            ipAct.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP;
            SendInput(1, &ipAct, sizeof(INPUT));

            //Then press down S
            ipAct.ki.wScan = moveKeys[2]; //Select S
            ipAct.ki.dwFlags = KEYEVENTF_SCANCODE;
            SendInput(1, &ipAct, sizeof(INPUT));
            return;
        }
        if (action == 3)//Left
        {
            ipAct.ki.wScan = moveKeys[3]; //Select A
            ipAct.ki.dwFlags = KEYEVENTF_SCANCODE;
            SendInput(1, &ipAct, sizeof(INPUT));
            
            ipAct.ki.wScan = moveKeys[5]; //Select E (powerslide mode)
            ipAct.ki.dwFlags = KEYEVENTF_SCANCODE;
            SendInput(1, &ipAct, sizeof(INPUT));
            
            return;
        }
        if (action == 4)//Right
        {
            ipAct.ki.wScan = moveKeys[4]; //Select D
            ipAct.ki.dwFlags = KEYEVENTF_SCANCODE;
            SendInput(1, &ipAct, sizeof(INPUT));

            ipAct.ki.wScan = moveKeys[5]; //Select E (powerslide mode)
            ipAct.ki.dwFlags = KEYEVENTF_SCANCODE;
            SendInput(1, &ipAct, sizeof(INPUT));
            return;
        }
        return;
    }
};

void actionMapSpeedDrift(int action, int lastAction)
{
    int moveKeys[6] = {0x11, 0x10, 0x1f, 0x1e, 0x20, 0x12}; //WQSADE keys

    // This structure will be used to create the keyboard
    // input event.
    INPUT ipAct; // Set up a generic keyboard event.
    ipAct.type = INPUT_KEYBOARD;
    ipAct.ki.wVk = 0; //We're doing scan codes instead
    ipAct.ki.time = 0;
    ipAct.ki.dwExtraInfo = 0;

    //First remove lastAction
    ipAct.ki.wScan = moveKeys[lastAction]; //Select last key
    ipAct.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP;
    SendInput(1, &ipAct, sizeof(INPUT));

    if ((lastAction == 2)||(lastAction == 3)) //OR conditional for removing power slide
    {   
        ipAct.ki.wScan = moveKeys[5];//Select powerslide
        ipAct.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP;
        SendInput(1, &ipAct, sizeof(INPUT));
    }

    //Start with a W
    ipAct.ki.wScan = moveKeys[0]; //Select W
    ipAct.ki.dwFlags = KEYEVENTF_SCANCODE;
    SendInput(1, &ipAct, sizeof(INPUT));

    if (action == 0)//Forward
    {
        return;
    }
    if (action == 1)//Power-Up
    {
        //first remove the W
        ipAct.ki.wScan = moveKeys[0]; //Select W
        ipAct.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP;
        SendInput(1, &ipAct, sizeof(INPUT));

        //Then fire power-up
        ipAct.ki.wScan = moveKeys[1]; //Select Q
        ipAct.ki.dwFlags = KEYEVENTF_SCANCODE;
        SendInput(1, &ipAct, sizeof(INPUT));
        return;
    }
    if (action == 2)//Reverse
    {   //first remove the W
        ipAct.ki.wScan = moveKeys[0]; //Select W
        ipAct.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP;
        SendInput(1, &ipAct, sizeof(INPUT));

        //Then press down S
        ipAct.ki.wScan = moveKeys[2]; //Select S
        ipAct.ki.dwFlags = KEYEVENTF_SCANCODE;
        SendInput(1, &ipAct, sizeof(INPUT));
        return;
    }
    if (action == 3)//Left
    {
        ipAct.ki.wScan = moveKeys[3]; //Select A
        ipAct.ki.dwFlags = KEYEVENTF_SCANCODE;
        SendInput(1, &ipAct, sizeof(INPUT));
        
        ipAct.ki.wScan = moveKeys[5]; //Select E (powerslide mode)
        ipAct.ki.dwFlags = KEYEVENTF_SCANCODE;
        SendInput(1, &ipAct, sizeof(INPUT));
        return;
    }
    if (action == 4)//Right
    {
        ipAct.ki.wScan = moveKeys[4]; //Select D
        ipAct.ki.dwFlags = KEYEVENTF_SCANCODE;
        SendInput(1, &ipAct, sizeof(INPUT));

        ipAct.ki.wScan = moveKeys[5]; //Select E (powerslide mode)
        ipAct.ki.dwFlags = KEYEVENTF_SCANCODE;
        SendInput(1, &ipAct, sizeof(INPUT));
        return;
    }
    return;
    
};

void reset()
{
    // Set up a generic keyboard event.
    INPUT ipReset;// This structure will be used to create the keyboard input event.
    ipReset.type = INPUT_KEYBOARD;
    ipReset.ki.time = 0;
    ipReset.ki.wVk = 0; //We're doing scan codes instead
    ipReset.ki.dwExtraInfo = 0;

    //Release W
    ipReset.ki.wScan = 0x11; //Select W
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP;
    SendInput(1, &ipReset, sizeof(INPUT));

    //press and release Esc
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE;
    ipReset.ki.wScan = 0x01; //ESC
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(250);

    //press and release DOWN
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_EXTENDEDKEY;
    ipReset.ki.wScan = MapVirtualKeyA(0x28, MAPVK_VK_TO_VSC);
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP | KEYEVENTF_EXTENDEDKEY;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(250);

    //press and release ENTER
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE;
    ipReset.ki.wScan = 0x1c; //ENTER
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(250);

    //press and release UP
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_EXTENDEDKEY;
    ipReset.ki.wScan = MapVirtualKeyA(0x26, MAPVK_VK_TO_VSC);
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP | KEYEVENTF_EXTENDEDKEY;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(250);

    //press and release ENTER
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE;
    ipReset.ki.wScan = 0x1c; //ENTER
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(250);

    //Press W
    ipReset.ki.wScan = 0x11; //Select W
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE;
    SendInput(1, &ipReset, sizeof(INPUT));

    return;
};

void quitResetMinmap(int mode, int course, int track)
{
    
    // Set up a generic keyboard event.
    INPUT ipReset;// This structure will be used to create the keyboard input event.
    ipReset.type = INPUT_KEYBOARD;
    ipReset.ki.time = 0;
    ipReset.ki.wVk = 0; //We're doing scan codes instead
    ipReset.ki.dwExtraInfo = 0;

    //press and release Esc
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE;
    ipReset.ki.wScan = 0x01; //ESC
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(500);

    //press and release DOWN (2x)
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_EXTENDEDKEY;
    ipReset.ki.wScan = MapVirtualKeyA(0x28, MAPVK_VK_TO_VSC);
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP | KEYEVENTF_EXTENDEDKEY;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(500);
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_EXTENDEDKEY;
    ipReset.ki.wScan = MapVirtualKeyA(0x28, MAPVK_VK_TO_VSC);
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP | KEYEVENTF_EXTENDEDKEY;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(500);

    //press and release ENTER
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE;
    ipReset.ki.wScan = 0x1c; //ENTER
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(500);

    //press and release UP
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_EXTENDEDKEY;
    ipReset.ki.wScan = MapVirtualKeyA(0x26, MAPVK_VK_TO_VSC);
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP | KEYEVENTF_EXTENDEDKEY;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(500);

    //press and release ENTER
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE;
    ipReset.ki.wScan = 0x1c; //ENTER
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(300);

    int i = 0; //reset counter
    while (i<mode)
    {
        //press and release DOWN
        ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_EXTENDEDKEY;
        ipReset.ki.wScan = MapVirtualKeyA(0x28, MAPVK_VK_TO_VSC);
        SendInput(1, &ipReset, sizeof(INPUT));
        ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP | KEYEVENTF_EXTENDEDKEY;
        SendInput(1, &ipReset, sizeof(INPUT));
        Sleep(500);
        i++;
    }

    //press and release ENTER
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE;
    ipReset.ki.wScan = 0x1c; //ENTER
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(300);

    //Course Select
    //press and release UPx2 
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_EXTENDEDKEY;
    ipReset.ki.wScan = MapVirtualKeyA(0x26, MAPVK_VK_TO_VSC);
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP | KEYEVENTF_EXTENDEDKEY;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(500);
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_EXTENDEDKEY;
    ipReset.ki.wScan = MapVirtualKeyA(0x26, MAPVK_VK_TO_VSC);
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP | KEYEVENTF_EXTENDEDKEY;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(500);

    while (i<course)
    {
        //Press Right
        ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_EXTENDEDKEY;
        ipReset.ki.wScan = MapVirtualKeyA(0x27, MAPVK_VK_TO_VSC);
        SendInput(1, &ipReset, sizeof(INPUT));
        ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP | KEYEVENTF_EXTENDEDKEY;
        SendInput(1, &ipReset, sizeof(INPUT));
        Sleep(500);
        i++;
    }

    //Track Select
    //press and release DOWN 
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_EXTENDEDKEY;
    ipReset.ki.wScan = MapVirtualKeyA(0x28, MAPVK_VK_TO_VSC);
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP | KEYEVENTF_EXTENDEDKEY;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(500);

    i = 1;
    while (i<track)
    {
        //Press Right
        ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_EXTENDEDKEY;
        ipReset.ki.wScan = MapVirtualKeyA(0x27, MAPVK_VK_TO_VSC);
        SendInput(1, &ipReset, sizeof(INPUT));
        ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP | KEYEVENTF_EXTENDEDKEY;
        SendInput(1, &ipReset, sizeof(INPUT));
        Sleep(500);
        i++;
    }
    //press and release DOWN
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_EXTENDEDKEY;
    ipReset.ki.wScan = MapVirtualKeyA(0x28, MAPVK_VK_TO_VSC);
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP | KEYEVENTF_EXTENDEDKEY;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(500);

    //press and release ENTER (2x)
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE;
    ipReset.ki.wScan = 0x1c; //ENTER
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(500);
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE;
    ipReset.ki.wScan = 0x1c; //ENTER
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(10000);

    //press and release "M" (2x)
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE;
    ipReset.ki.wScan = 0x32; //M
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(500);
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE;
    ipReset.ki.wScan = 0x32; //M
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(500);

    return;
}

void quitResetSpeed(int mode, int course, int track)
{
    
    // Set up a generic keyboard event.
    INPUT ipReset;// This structure will be used to create the keyboard input event.
    ipReset.type = INPUT_KEYBOARD;
    ipReset.ki.time = 0;
    ipReset.ki.wVk = 0; //We're doing scan codes instead
    ipReset.ki.dwExtraInfo = 0;

//press and release Esc
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE;
    ipReset.ki.wScan = 0x01; //ESC
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(500);

    //press and release DOWN (2x)
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_EXTENDEDKEY;
    ipReset.ki.wScan = MapVirtualKeyA(0x28, MAPVK_VK_TO_VSC);
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP | KEYEVENTF_EXTENDEDKEY;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(500);
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_EXTENDEDKEY;
    ipReset.ki.wScan = MapVirtualKeyA(0x28, MAPVK_VK_TO_VSC);
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP | KEYEVENTF_EXTENDEDKEY;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(500);

    //press and release ENTER
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE;
    ipReset.ki.wScan = 0x1c; //ENTER
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(500);

    //press and release UP
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_EXTENDEDKEY;
    ipReset.ki.wScan = MapVirtualKeyA(0x26, MAPVK_VK_TO_VSC);
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP | KEYEVENTF_EXTENDEDKEY;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(500);

    //press and release ENTER
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE;
    ipReset.ki.wScan = 0x1c; //ENTER
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(300);

    int i = 0; //reset counter
    while (i<mode)
    {
        //press and release DOWN
        ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_EXTENDEDKEY;
        ipReset.ki.wScan = MapVirtualKeyA(0x28, MAPVK_VK_TO_VSC);
        SendInput(1, &ipReset, sizeof(INPUT));
        ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP | KEYEVENTF_EXTENDEDKEY;
        SendInput(1, &ipReset, sizeof(INPUT));
        Sleep(500);
        i++;
    }

    //press and release ENTER
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE;
    ipReset.ki.wScan = 0x1c; //ENTER
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(300);

    //Course Select
    //press and release UPx2 
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_EXTENDEDKEY;
    ipReset.ki.wScan = MapVirtualKeyA(0x26, MAPVK_VK_TO_VSC);
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP | KEYEVENTF_EXTENDEDKEY;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(500);
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_EXTENDEDKEY;
    ipReset.ki.wScan = MapVirtualKeyA(0x26, MAPVK_VK_TO_VSC);
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP | KEYEVENTF_EXTENDEDKEY;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(500);

    while (i<course)
    {
        //Press Right
        ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_EXTENDEDKEY;
        ipReset.ki.wScan = MapVirtualKeyA(0x27, MAPVK_VK_TO_VSC);
        SendInput(1, &ipReset, sizeof(INPUT));
        ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP | KEYEVENTF_EXTENDEDKEY;
        SendInput(1, &ipReset, sizeof(INPUT));
        Sleep(500);
        i++;
    }

    //Track Select
    //press and release DOWN 
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_EXTENDEDKEY;
    ipReset.ki.wScan = MapVirtualKeyA(0x28, MAPVK_VK_TO_VSC);
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP | KEYEVENTF_EXTENDEDKEY;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(500);

    i = 1;
    while (i<track)
    {
        //Press Right
        ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_EXTENDEDKEY;
        ipReset.ki.wScan = MapVirtualKeyA(0x27, MAPVK_VK_TO_VSC);
        SendInput(1, &ipReset, sizeof(INPUT));
        ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP | KEYEVENTF_EXTENDEDKEY;
        SendInput(1, &ipReset, sizeof(INPUT));
        Sleep(500);
        i++;
    }
    //press and release DOWN
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_EXTENDEDKEY;
    ipReset.ki.wScan = MapVirtualKeyA(0x28, MAPVK_VK_TO_VSC);
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP | KEYEVENTF_EXTENDEDKEY;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(500);

    //press and release ENTER (2x)
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE;
    ipReset.ki.wScan = 0x1c; //ENTER
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(500);
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE;
    ipReset.ki.wScan = 0x1c; //ENTER
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(10000);

    //press and release "M" (1x)
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE;
    ipReset.ki.wScan = 0x32; //M
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(500);

    return;
}

void firstRunMinmap(int mode, int course, int track)
{

    // Set up a generic keyboard event.
    INPUT ipReset;// This structure will be used to create the keyboard input event.
    ipReset.type = INPUT_KEYBOARD;
    ipReset.ki.time = 0;
    ipReset.ki.wVk = 0; //We're doing scan codes instead
    ipReset.ki.dwExtraInfo = 0;

    int i = 0; //reset counter
    while (i<mode)
    {
        //press and release DOWN
        ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_EXTENDEDKEY;
        ipReset.ki.wScan = MapVirtualKeyA(0x28, MAPVK_VK_TO_VSC);
        SendInput(1, &ipReset, sizeof(INPUT));
        ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP | KEYEVENTF_EXTENDEDKEY;
        SendInput(1, &ipReset, sizeof(INPUT));
        Sleep(500);
        i++;
    }

    //press and release ENTER
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE;
    ipReset.ki.wScan = 0x1c; //ENTER
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(300);

    //Course Select
    //press and release UPx2 
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_EXTENDEDKEY;
    ipReset.ki.wScan = MapVirtualKeyA(0x26, MAPVK_VK_TO_VSC);
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP | KEYEVENTF_EXTENDEDKEY;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(500);
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_EXTENDEDKEY;
    ipReset.ki.wScan = MapVirtualKeyA(0x26, MAPVK_VK_TO_VSC);
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP | KEYEVENTF_EXTENDEDKEY;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(500);

    while (i<course)
    {
        //Press Right
        ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_EXTENDEDKEY;
        ipReset.ki.wScan = MapVirtualKeyA(0x27, MAPVK_VK_TO_VSC);
        SendInput(1, &ipReset, sizeof(INPUT));
        ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP | KEYEVENTF_EXTENDEDKEY;
        SendInput(1, &ipReset, sizeof(INPUT));
        Sleep(500);
        i++;
    }

    //Track Select
    //press and release DOWN 
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_EXTENDEDKEY;
    ipReset.ki.wScan = MapVirtualKeyA(0x28, MAPVK_VK_TO_VSC);
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP | KEYEVENTF_EXTENDEDKEY;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(500);

    i = 1;
    while (i<track)
    {
        //Press Right
        ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_EXTENDEDKEY;
        ipReset.ki.wScan = MapVirtualKeyA(0x27, MAPVK_VK_TO_VSC);
        SendInput(1, &ipReset, sizeof(INPUT));
        ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP | KEYEVENTF_EXTENDEDKEY;
        SendInput(1, &ipReset, sizeof(INPUT));
        Sleep(500);
        i++;
    }
    //press and release DOWN
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_EXTENDEDKEY;
    ipReset.ki.wScan = MapVirtualKeyA(0x28, MAPVK_VK_TO_VSC);
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP | KEYEVENTF_EXTENDEDKEY;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(500);

    //press and release ENTER (2x)
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE;
    ipReset.ki.wScan = 0x1c; //ENTER
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(500);
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE;
    ipReset.ki.wScan = 0x1c; //ENTER
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(10000);

    //press and release "M" (2x)
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE;
    ipReset.ki.wScan = 0x32; //M
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(500);
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE;
    ipReset.ki.wScan = 0x32; //M
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(500);

    //press and release "V"
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE;
    ipReset.ki.wScan = 0x2F;
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(500);

    return;
}

void firstRunSpeed(int mode, int course, int track)
{
    
    // Set up a generic keyboard event.
    INPUT ipReset;// This structure will be used to create the keyboard input event.
    ipReset.type = INPUT_KEYBOARD;
    ipReset.ki.time = 0;
    ipReset.ki.wVk = 0; //We're doing scan codes instead
    ipReset.ki.dwExtraInfo = 0;

    int i = 0; //reset counter
    while (i<mode)
    {
        //press and release DOWN
        ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_EXTENDEDKEY;
        ipReset.ki.wScan = MapVirtualKeyA(0x28, MAPVK_VK_TO_VSC);
        SendInput(1, &ipReset, sizeof(INPUT));
        ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP | KEYEVENTF_EXTENDEDKEY;
        SendInput(1, &ipReset, sizeof(INPUT));
        Sleep(500);
        i++;
    }

    //press and release ENTER
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE;
    ipReset.ki.wScan = 0x1c; //ENTER
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(300);

    //Course Select
    //press and release UPx2 
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_EXTENDEDKEY;
    ipReset.ki.wScan = MapVirtualKeyA(0x26, MAPVK_VK_TO_VSC);
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP | KEYEVENTF_EXTENDEDKEY;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(500);
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_EXTENDEDKEY;
    ipReset.ki.wScan = MapVirtualKeyA(0x26, MAPVK_VK_TO_VSC);
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP | KEYEVENTF_EXTENDEDKEY;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(500);

    i = 1;
    while (i<course)
    {
        //Press Right
        ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_EXTENDEDKEY;
        ipReset.ki.wScan = MapVirtualKeyA(0x27, MAPVK_VK_TO_VSC);
        SendInput(1, &ipReset, sizeof(INPUT));
        ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP | KEYEVENTF_EXTENDEDKEY;
        SendInput(1, &ipReset, sizeof(INPUT));
        Sleep(500);
        i++;
    }

    //Track Select
    //press and release DOWN 
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_EXTENDEDKEY;
    ipReset.ki.wScan = MapVirtualKeyA(0x28, MAPVK_VK_TO_VSC);
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP | KEYEVENTF_EXTENDEDKEY;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(500);

    i = 1;
    while (i<track)
    {
        //Press Right
        ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_EXTENDEDKEY;
        ipReset.ki.wScan = MapVirtualKeyA(0x27, MAPVK_VK_TO_VSC);
        SendInput(1, &ipReset, sizeof(INPUT));
        ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP | KEYEVENTF_EXTENDEDKEY;
        SendInput(1, &ipReset, sizeof(INPUT));
        Sleep(500);
        i++;
    }

    //press and release DOWN
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_EXTENDEDKEY;
    ipReset.ki.wScan = MapVirtualKeyA(0x28, MAPVK_VK_TO_VSC);
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP | KEYEVENTF_EXTENDEDKEY;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(500);

    //press and release ENTER (2x)
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE;
    ipReset.ki.wScan = 0x1c; //ENTER
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(500);
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE;
    ipReset.ki.wScan = 0x1c; //ENTER
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(10000);

    //press and release "M" (1x)
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE;
    ipReset.ki.wScan = 0x32; //M
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(500);

    //press and release "V"
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE;
    ipReset.ki.wScan = 0x2F;
    SendInput(1, &ipReset, sizeof(INPUT));
    ipReset.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP;
    SendInput(1, &ipReset, sizeof(INPUT));
    Sleep(500);

    return;
}

struct MyData
{
    float x, y;

    MyData() : x(0), y(0)
    {
    }

    MyData(float x, float y) : x(x), y(y)
    {
    }

    void print()
    {
        printf("%f, %f\n", x, y);
    }
};

PYBIND11_MODULE (pybind11module, module)
{   // optional module docstring
    module.doc () = "LRKeymapper";
    // define add function
    module.def("actionMapMinmap", &actionMapMinmap, "actionMapMinmap");
    module.def("actionMapSpeed", &actionMapSpeed, "actionMapSpeed");
    module.def("actionMapMinmapDrift", &actionMapMinmapDrift, "actionMapMinmapDrift");
    module.def("actionMapSpeedDrift", &actionMapSpeedDrift, "actionMapSpeedDrift");
    module.def("reset", &reset, "reset");
    module.def("quitResetMinmap", &quitResetMinmap, "quitResetMinmap");
    module.def("quitResetSpeed", &quitResetSpeed, "quitResetSpeed");
    module.def("firstRunMinmap", &firstRunMinmap, "firstRunMinmap");
    module.def("firstRunSpeed", &firstRunSpeed, "firstRunSpeed");

    pybind11::class_<MyData>(module, "MyData")
        .def(pybind11::init<>())
        .def(pybind11::init<float, float>(), "constructor 2", pybind11::arg("x"), pybind11::arg("y"))
        .def("print", &MyData::print)
        .def_readwrite("x", &MyData::x)
        .def_readwrite("y", &MyData::y)
    ;
}