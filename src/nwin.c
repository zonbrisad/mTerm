/**
 *---------------------------------------------------------------------------
 * @brief    Main window handler
 *
 * @file     nwin.c
 * @author   Peter Malmberg <peter.malmberg@gmail.com>
 * @date     2017-11-08
 * @license  GPLv2
 *
 *---------------------------------------------------------------------------
 *
 *
 */


// Includes -----------------------------------------------------------------

#include <ncurses.h>
#include "nwin.h"
#include "uart.h"

// Macros -------------------------------------------------------------------


// Variables ----------------------------------------------------------------

WINDOW    *mainWin = NULL;
WINDOW    *infoWin = NULL;


// Prototypes ---------------------------------------------------------------


// Code ---------------------------------------------------------------------


void createWindows() {
  if (infoWin != NULL) {
    delwin(infoWin);
  }
  
  if (mainWin != NULL) {
    delwin(mainWin);
  }
  
  infoWin = newwin(1,COLS, LINES-1, 0);
  mainWin = newwin(LINES-1,COLS, 0, 0);
  scrollok(mainWin, TRUE);  
}

void winChangeHdl(int x) {
//  wprintw(mainWin, "Winchange\n");
  createWindows(); 
//  updateInfoWin(mDev);
}

void sigintHdl(int sig) {
//  g_main_loop_quit(mLoop);
}

void updateInfoWin(uart *dev) {
  wclear(infoWin);
  wprintw(infoWin, " %-20s %6d %6d Rx  %6d Tx", dev->device, dev->bitrate, dev->rxCnt, dev->txCnt);
  wrefresh(infoWin);
}


void safeExit(int x) {
  
   
  delwin(mainWin);
  delwin(infoWin);
  endwin();        
  
 
}

void nwin_init(void) {
  
   initscr();            // Start curses mode      
	  refresh();            // Print it on to the real screen 
	  //cbreak();             // turn off input buffering
	  noecho();             // turn off automatic echoing
	  //raw();                // raw mode
	  //keypad(stdscr, TRUE); // enables F1, F2 etc
	  curs_set(2);          // make cursor visible
	
  
  createWindows();
}
