/**
 *---------------------------------------------------------------------------
 *
 * @brief Makeplate GLIB example
 *
 * @file    main.c
 * @author  Peter Malmberg <peter.malmberg@gmail.com>
 * @date    2015-05-19 01:20:00
 *
 *---------------------------------------------------------------------------
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <signal.h>
#include <glib-2.0/glib.h>
#include <glib-unix.h>
#include <termios.h>
#include <sys/types.h>
#include <fcntl.h>
#include <ncurses.h>
#include <signal.h>

#include "lua.h"
#include "lauxlib.h"

#include "gp_log.h"
#include "termkey.h"
#include "uart.h"


// Defines -------------------------------------------------------------------
 
#define VERSION     "0.1"
#define DESCRIPTION "- a serial port terminal program"
#define LOGFILE     "mterm.log"

 #define BAUDRATE B38400
 #define MODEMDEVICE "/dev/ttyUSB0"


// Variables -----------------------------------------------------------------
 
WINDOW    *mainWin = NULL; 
WINDOW    *infoWin = NULL;

GTimer    *timer;
GThread   *thread1;
GThread   *thread2;
GMainLoop *mLoop;

static gboolean opt_verbose   = FALSE;
static gboolean opt_version   = FALSE;
static gboolean opt_quiet     = FALSE;
static gboolean opt_daemon    = FALSE;
//static gboolean opt_webtest    = FALSE;

static int opt_bitrate = -1;
static char *opt_port  = NULL;
static char *opt_log   = NULL;

static TermKey *tk;
static int timeout_id;
static uart *dev  = NULL;
static uart *mDev = NULL;

static GOptionEntry entries[] = {
//   { "verbose",  'v', 0, G_OPTION_ARG_NONE,     &opt_verbose,    "Be verbose output",    NULL },
   { "version",  'v', 0, G_OPTION_ARG_NONE,     &opt_version,    "Output version info",  NULL },
   { "quiet",    'q', 0, G_OPTION_ARG_NONE,     &opt_quiet,      "No output to console", NULL },
   { "daemon",    0,  0, G_OPTION_ARG_NONE,     &opt_daemon,     "Run as daemon",      NULL },
   { "bitrate",  'b', 0, G_OPTION_ARG_INT,      &opt_bitrate,    "Bitrate",              NULL },
 //  { "str",      's', 0, G_OPTION_ARG_STRING,   opt_str,         "Bitrate",              NULL },
   { "port",     'p', 0, G_OPTION_ARG_FILENAME, &opt_port,       "Serial port device",   NULL },
   { "log",      'l', 0, G_OPTION_ARG_FILENAME, &opt_log,        "Log file",   NULL },
   { NULL }
};




// Prototypes ---------------------------------------------------------------

void updateInfoWin(uart *dev);


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
  updateInfoWin(mDev);
}

void sigintHdl(int sig) {
  g_main_loop_quit(mLoop);
}

void updateInfoWin(uart *dev) {
  wclear(infoWin);
  wprintw(infoWin, " %-20s %6d %6d Rx  %6d Tx", dev->device, dev->bitrate, dev->rxCnt, dev->txCnt);
  wrefresh(infoWin);
}

static void on_key(TermKey *tk, TermKeyKey *key, uart *dev)
{
  char buf[50];
  termkey_strfkey(tk, buf, sizeof(buf), key, TERMKEY_FORMAT_VIM);
  wprintw(mainWin, "%s\n", buf);
  wrefresh(mainWin);
  //buf[0]='A';
  uart_send(dev, buf, 1);
  
  updateInfoWin(dev);
}

static gboolean key_timer(gpointer data)
{
//  TermKeyKey key;
/*
  if(termkey_getkey_force(tk, &key) == TERMKEY_RES_KEY)
    on_key(tk, &key);
*/
  return FALSE;
}
static gboolean stdin_io(GIOChannel *source, GIOCondition condition, gpointer data) {
  uart *dev;
  
  dev = (uart*) data;
  
  if(condition && G_IO_IN) {
    if(timeout_id)
      g_source_remove(timeout_id);

    termkey_advisereadable(tk);

    TermKeyResult ret;
    TermKeyKey key;
    while((ret = termkey_getkey(tk, &key)) == TERMKEY_RES_KEY) {
      on_key(tk, &key, dev);
     
    }

    if(ret == TERMKEY_RES_AGAIN)
      timeout_id = g_timeout_add(termkey_get_waittime(tk), key_timer, NULL);
  }

  
  return TRUE;
}

void safeExit(int x) {
  delwin(mainWin);
  delwin(infoWin);
  endwin();
  
  if (tk) {
    termkey_destroy(tk); 
  }
  
  gp_log_close();
  
  uart_close(dev);
  
//  printf("X\n");
  exit(x);
}


static gboolean uart_io(GIOChannel *source, GIOCondition condition, gpointer data) {
//  static char buf[255];
//  int res;
  uart *dev;
  
  dev = (uart*) data;
  
  if(condition && G_IO_IN) {
    uart_read(dev);
    //res = read(dev->fd,buf,255);   /* returns after 5 chars have been input */
    
    dev->buf[dev->lastRx]=0;               /* so we can printf... */
    wprintw(mainWin, ":%3d:%s\n", dev->lastRx, dev->buf);
    wrefresh(mainWin);
    
    updateInfoWin(dev);
    //if (buf[0]=='z') STOP=TRUE;
    //printf("received\n");

  }

  return TRUE;
}

int main(int argc, char *argv[]) {
  GError *error = NULL;
  GOptionContext *context;
  int err;
	
  // init log system
  gp_log_init(LOGFILE);
  gp_log_set_verbose(TRUE);
  gp_log_set_verbose_mask(GP_ERROR);
	
  // parse command line arguments
  context = g_option_context_new (DESCRIPTION);
  g_option_context_add_main_entries (context, entries, NULL);
  if (!g_option_context_parse (context, &argc, &argv, &error)) {
    g_print ("option parsing failed: %s\n", error->message);
    exit (1);
  }

  // print version information
  if (opt_version) {
    printf("Program version %s\nBuild ("__DATE__" "__TIME__")\n", VERSION);
    safeExit(1);
  }
	
  // enable verbose mode
  if (opt_verbose) {
    gp_log_set_verbose(TRUE);  
  }
	
  //uartTest();
  //exit(0);
  
//  printf("Str: %s\n", opt_str);
	
//  printf("Ett litet testprogram.\n");
	
//  lua_State *L = luaL_newstate();
//  luaL_openlibs(L);
//  luaL_dofile(L, "test.lua");
  //luaL_close(L);
	
  // Open serial port
  if (opt_port == NULL) {
    printf("Serial port must be given (-p /dev/ttyXX)\n");
    safeExit(1);
  }
  
  // check if bitrate is given
  if (opt_bitrate == -1) {
    printf("Bitrate must be given (-b XXX)\n");
    uart_printBitrates();
    safeExit(1);
  }
  
  // check if bitrate is correct
  if (!uart_isBitrate(opt_bitrate)) {
    printf("Bitrate wrong se bellow (%d)\n", opt_bitrate);
    uart_printBitrates();
    safeExit(1);
  }
          
  dev = uart_new(opt_port, opt_bitrate);
  
  err = uart_open(dev);
  
  if (err != UART_SUCCESS) {
    printf("Could not open serialport %s\n", dev->device);
    safeExit(1);
  }
  
  mDev = dev;
  
  initscr();            // init ncurses
  //raw();                // raw mode
  cbreak();
  
  
  // 
  createWindows();
  
  //wprintw(mainWin, "Testing COLS %d  LINES %d", COLS, LINES);
  wrefresh(mainWin);
  
  tk = termkey_new(0, 0);

  if(!tk) {
    fprintf(stderr, "Cannot allocate termkey instance\n");
    safeExit(1);
  }
  
  // Create main loop
  mLoop = g_main_loop_new(NULL, FALSE);
  
  // Handle window change event
  signal(SIGWINCH, winChangeHdl);
  
  // handle ctrl-c 
  signal(SIGINT,   sigintHdl);
  
  updateInfoWin(dev);
  
  g_io_add_watch(g_io_channel_unix_new(dev->fd), G_IO_IN, uart_io, (gpointer) dev);
  
  // Add keyboard input 
  g_io_add_watch(g_io_channel_unix_new(0), G_IO_IN, stdin_io, (gpointer) dev);
   
  g_main_loop_run(mLoop);

	safeExit(0);
}
