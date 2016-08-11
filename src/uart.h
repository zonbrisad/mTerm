/**
 *---------------------------------------------------------------------------
 * @brief   Linux UART controll library
 *
 * @file    uart.h
 * @author  Peter Malmberg <peter.malmberg@gmail.com>
 * @date    2016-07-24
 * @licence GPLv2
 *
 *---------------------------------------------------------------------------
 */

#ifndef UART_H
#define UART_H

#ifdef __cplusplus
extern "C" {
#endif

// Includes ---------------------------------------------------------------
#include <termios.h>
    
#include "gp_log.h"
    
// Macros -----------------------------------------------------------------

#define BUFSIZE 1024    
    
// Typedefs ---------------------------------------------------------------

typedef struct {
  int fd;
  char device[64];
  struct termios oldtty;
  struct termios tty;
  int bitrate;
  int rxCnt;
  int txCnt;
  int lastRx;
  int lastTx;
  char buf[BUFSIZE];
} uart;

typedef enum {
  UART_SUCCESS = 0,
  UART_ERROR_NO_DEVICE,
  UART_ERROR_BITRATE          
} UART_ERROR;

typedef struct {
  int bitrate;
  int tc_bitrate;
} UART_BITRATE;

        
// Variables --------------------------------------------------------------

// Functions --------------------------------------------------------------


uart *uart_new(char *device, int bitrate);

UART_ERROR uart_open(uart *dev);

void uart_setBaudRate(uart *dev, int baudrate);

void uart_close(uart *dev);

UART_ERROR uart_read(uart *dev);

UART_ERROR uart_send(uart *dev, char *buf, int count);


int uart_isBitrate(int bitrate);

int uart_getTcBitrate(int bitrate);

void uart_printBitrates();

 
#ifdef __cplusplus
} //end brace for extern "C"
#endif
#endif

