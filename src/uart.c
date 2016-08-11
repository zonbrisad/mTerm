/**
 *---------------------------------------------------------------------------
 * @brief   Linux UART controll library
 *
 * @file    uart.c
 * @author  Peter Malmberg <peter.malmberg@gmail.com>
 * @date    2016-07-24
 * @licence GPLv2
 *
 *---------------------------------------------------------------------------
 */

// Includes ---------------------------------------------------------------

#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/types.h>
#include <string.h>
#include <unistd.h>

#include "uart.h"

// Macros -----------------------------------------------------------------

// Variables --------------------------------------------------------------


static UART_BITRATE br2br[] = {
  {     50,       B50 },
  {     75,       B75 },
  {     110,     B110 },
  {     134,     B134 },
  {     150,     B150 },
  {     200,     B200 },
  {     300,     B300 },
  {     600,     B600 },
  {    1200,    B1200 },
  {    1800,    B1800 },
  {    2400,    B2400 },
  {    4800,    B4800 },
  {    9600,    B9600 },
  {   19200,   B19200 },
  {   38400,   B38400 },
  {   57600,   B57600 },
  {  115200,  B115200 },
  {  230400,  B230400 },
  {  460800,  B460800 },
  {  921600,  B921600 },
  { 1000000, B1000000 },
  { 1152000, B1152000 },
  { 1500000, B1500000 },
  { 2000000, B2000000 },
  { 2500000, B2500000 },
  { 3000000, B3000000 },
  { 3500000, B3500000 },
  { 4000000, 43000000 },
  {       0,        0 }
};
// Prototypes -------------------------------------------------------------

// Code -------------------------------------------------------------------


int uart_set_attribs(uart *dev) {
  return 0;  
}

UART_ERROR uart_open(uart *dev) {
  speed_t tcBitrate;
  dev->fd = open(dev->device, O_RDWR | O_NOCTTY | O_NDELAY); 
  
  if (dev->fd <0) {
    return UART_ERROR_NO_DEVICE;
  }
  
  tcgetattr(dev->fd,&dev->oldtty); /* save current port settings */

  bzero(&dev->tty, sizeof(dev->tty));
  
  tcBitrate = (speed_t)uart_getTcBitrate(dev->bitrate);
  
  cfsetospeed(&dev->tty, tcBitrate);
  cfsetispeed(&dev->tty, tcBitrate);
  
  dev->tty.c_cflag |= (CLOCAL | CREAD);  // ignore modem controls
  dev->tty.c_cflag |= CS8;               // 8 bit characters
  dev->tty.c_cflag &= ~CRTSCTS;          // no hardware flowcontrol
  dev->tty.c_cflag &= ~PARENB;           // no parity bit 
  dev->tty.c_cflag &= ~CSTOPB;           // only need 1 stop bit 

  /* setup for non-canonical mode */
  dev->tty.c_iflag &= ~(IGNBRK | BRKINT | PARMRK | ISTRIP | INLCR | IGNCR | ICRNL | IXON);
  dev->tty.c_lflag &= ~(ECHO | ECHONL | ICANON | ISIG | IEXTEN);
  dev->tty.c_oflag = ~OPOST;

  dev->tty.c_cc[VTIME]    = 0;   /* inter-character timer unused */
  dev->tty.c_cc[VMIN]     = 0;   /* blocking read until x chars received */

  tcflush(dev->fd, TCIFLUSH);
  tcsetattr(dev->fd,TCSANOW,&dev->tty);
    
  return UART_SUCCESS;  
}

uart *uart_new(char *device, int bitrate) {
  uart *dev;  
  
  dev = malloc(sizeof(uart));
  
  dev->bitrate = bitrate;
  strncpy(dev->device, device, 64);
    
  return dev;  
}

void uart_setBaudRate(uart *dev, int baudrate) {
  
}

void uart_close(uart *dev) {
  if (dev==NULL) {
    return;
  }
  tcsetattr(dev->fd,TCSANOW,&dev->oldtty);
  close(dev->fd);
}


UART_ERROR uart_read(uart *dev) {
  int res;
  res = read(dev->fd, dev->buf, BUFSIZE);   /* returns after 5 chars have been input */
  if (res>0) {
    dev->rxCnt += res; 
  }
  dev->lastRx = res;
  return UART_SUCCESS;
}

UART_ERROR uart_send(uart *dev, char *buf, int count) {
  int res;
  res = write(dev->fd, buf, count);
  tcflush(dev->fd, TCIOFLUSH);
  dev->txCnt += res;
  return UART_SUCCESS;
}

int uart_isBitrate(int bitrate) {
  int i;
  i = 0;
  while (br2br[i].bitrate != 0 ) {
    if (br2br[i].bitrate == bitrate)
      return TRUE;
    i++;
  }
  return FALSE;
}

int uart_getTcBitrate(int bitrate) {
  int i;
  i = 0;
  while (br2br[i].bitrate != 0 ) {
    if (br2br[i].bitrate == bitrate)
      return br2br[i].tc_bitrate;
    i++;
  }
  return -1;
}

void uart_printBitrates() {
  int i;
  i = 0;
  while (br2br[i].bitrate != 0 ) {
    printf("%7d bits/s\n", br2br[i].bitrate);
    i++;
  }
}
