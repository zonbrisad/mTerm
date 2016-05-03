/* 
 * File:   gp_log.h
 * Author: pmg
 *
 * Created on April 14, 2015, 6:34 PM
 */

#ifndef GP_LOG_H
#define	GP_LOG_H

#include <glib-2.0/glib.h>

#ifdef	__cplusplus
extern "C" {
#endif

  /**
   * Init log system.
   */
  void gp_log_init(char *logfile);
	
	
	/**
	 *  Set verbose mode
	 */
	void gp_log_set_verbose(gboolean v);

  /**
   * Print log to stdout.
   */
  void gp_log_print();
  
  
	
	/**
	 * Close down log system
	 */
	void gp_log_close();

#ifdef	__cplusplus
}
#endif

#endif	/* GP_LOG_H */

