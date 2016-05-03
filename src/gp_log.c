
#include <syslog.h>
#include <stdio.h>
#include <glib-2.0/glib.h>
#include <glib/gstdio.h>

#include "Def.h"
#include "gp_log.h"


gboolean gp_verbose=FALSE;
gboolean gp_syslog=FALSE;
gboolean gp_debug=FALSE;
gboolean gp_noColor=FALSE;

int gp_maxSize;
int gp_logSize;

char *gp_logFile;
char *gp_logDir;

FILE *gpLogFile = NULL;
char *gpLogFilename;

static void gp_log_handler(const gchar *log_domain,
                   GLogLevelFlags log_level,
                   const gchar *message,
                   gpointer user_data );


void gp_log_set_verbose(gboolean v) {
  gp_verbose = v;
}

void gp_log_init(char *logfile) {
	GStatBuf st;
	
	gpLogFilename = logfile;
	gp_log_set_verbose(FALSE);
	
	/* Set handler for all levels */
  g_log_set_handler(G_LOG_DOMAIN, G_LOG_LEVEL_MASK | G_LOG_LEVEL_ERROR | G_LOG_FLAG_FATAL, gp_log_handler, NULL);
	
	gpLogFile = g_fopen(logfile, "a");
  if (gpLogFile==NULL) {
    g_warning("Could not open file for message logging\n");
		return;
  }
	
  g_stat(gpLogFilename, &st);
	gp_logSize = st.st_size;
	g_debug("Logfile size: %d\n", gp_logSize);

}

void gp_log_close() {
  fclose(gpLogFile);  
}

static void gp_log_handler(const gchar *log_domain,
                           GLogLevelFlags log_level,
                           const gchar *message,
                           gpointer user_data )
{
	char *color;
  char *level;
  GDateTime *dt;
  char *dateTime;
  int i;
    
  color = E_WHITE;
  level = "    ";
  switch (log_level & G_LOG_LEVEL_MASK) {
	 case G_LOG_LEVEL_WARNING:  color = E_BR_YELLOW;  level = "warn"; break;
	 case G_LOG_LEVEL_ERROR:    color = E_BR_RED;     level = "err "; break;
	 case G_LOG_LEVEL_CRITICAL: color = E_WONR;       level = "crit"; break;
	 case G_LOG_LEVEL_DEBUG:    color = E_BR_GREEN;   level = "dbg "; break;
	 case G_LOG_LEVEL_INFO:     color = E_WHITE;      level = "info"; break;
	 case G_LOG_LEVEL_MESSAGE:  color = E_BR_CYAN;    level = "msg "; break;
   default: color = E_WHITE; level="dflt"; break; 
  }
  
  // date and time information
  dt = g_date_time_new_now_local();
  dateTime = g_date_time_format(dt,"%Y-%m-%d %k:%M:%S");
  
  // print to stdout if in verbose mode
  if ( gp_verbose ) {
    printf("%s [%s%s%s] %s",dateTime,color,level,E_END,message);
  }
  
  if (gp_logSize>gp_maxSize) {
  	//g_see
  }

  // write to logfile if existing
  if (gpLogFile!=NULL) {
    i = fprintf(gpLogFile, "%s [%s] %s", dateTime, level, message);
    if (i>0)
    	gp_logSize += i;
  }
  g_free(dateTime);
  
  return ;
}

void gp_log_print() {

}
