#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------
# 
# C/C++ template generator
#
# File:    ctemplate.py
# Author:  Peter Malmberg <peter.malmberg@gmail.com>
# Date:    2016-02-19
# Version: 0.3
# Python:  >=3
# Licence: MIT
# 
# -----------------------------------------------------------------------
# History
# - Ver 0.3 
# Major rewrite for better code generation
#
# Todo 
#
# Imports -------------------------------------------------------------------

import sys
import os 
import traceback
import logging
import argparse
from  pathlib import Path
from datetime import datetime, date, time

# Settings ------------------------------------------------------------------

AppName     = "ctemplate"
AppVersion  = "0.2"
AppLicense  = "MIT"
AppAuthor   = "Peter Malmberg <peter.malmberg@gmail.com>"

# Uncomment to use logfile
#LogFile     = "pyplate.log"

# Code ----------------------------------------------------------------------

# 
# Configuration class
#
class CConf():
    main       = False
    gtk        = False
    qt         = False
    signals    = False
    sigint     = False
    author     = ""
    license    = ""
    brief      = ""
    date       = ""
    org        = ""
    isCpp      = False
    moduleName = ""
    
    name       = ""
    email      = ""
    license    = ""
    org        = ""
    author     = ""
    
    def __init__(self):
        self.date = datetime.now().strftime("%Y-%m-%d")
        self.bp()

    # Get bashplates environment variables (if available)
    def bp(self):
        self.name    = os.getenv('BP_NAME',    "")
        self.email   = os.getenv('BP_EMAIL',   "")
        self.license = os.getenv('BP_LICENSE', "")
        self.org     = os.getenv('BP_ORG',     "")
        self.author  = self.name+" <"+self.email+">"
        
    def ask(self, module):
        print("Creating new "+module)
    
        if self.moduleName == "":
            self.moduleName = input("Enter "+module+" name(no extention):>")
        
        if self.brief == "":
            self.brief = input("Enter brief description:> ")

    
class CFile():
    moduleName = ""
    fileName   = ""

    header     = ""
    include    = ""
    defines    = ""
    variables  = ""
    prototypes = ""
    code       = ""
    main       = ""

    buf        = ""
    isHeader   = False 
    isCpp      = False
    
    def __init__(self, conf, isHeader):
        self.conf       = conf
        self.moduleName = conf.moduleName
        self.isHeader   = isHeader
        self.isCpp      = conf.isCpp
        
        if isHeader: 
            self.fileName = self.moduleName + ".h"
        else:
            if self.isCpp:
                self.fileName = self.moduleName + ".cpp"
            else:
                self.fileName = self.moduleName + ".c"
                
    def addHeader(self):
        hFileName = scriptPath + "/header.h"
        hFile = Path(hFileName)

        if hFile.is_file():            # Using external header file if existing
            try:
                f = open(hFileName, 'r+')
            except IOError:
                logging.debug("Could not open file %s" % (hFileName))
                exit()
            except:
                print ("Unexpected error:", sys.exc_info()[0])
                exit()
        
                self.header = f.read()
        else:                             # Using internal header example
            self.header = headerExample
        return
    
    def addInclude(self, fileName, local = False):
        if local:
            self.include += ("#include \""+fileName+"\"\n")
        else:
            self.include += ("#include <"+fileName+">\n")
    
    def addDefine(self, name, value):
        self.defines += ("#define  " + name + "  "+ value + "\n")

    def addVariable(self, name):
        self.variables += name

    def addPrototype(self, prototype):
        self.prototypes += prototype
    
    def addSection(self, desc):
        line = '-' * (73 - len(desc))
        self.buf += "\n// " + desc + " " + line + "\n\n"
        
    def addSentinelBegin(self, sentinel):
        self.buf +=  \
        "#ifndef "+sentinel+"_H\n"      \
        "#define "+sentinel+"_H\n\n" 
    
    def addSentinelEnd(self):
        self.buf += "#endif\n\n"

    def addCppSentinel(self):
        self.buf += \
        "#ifdef __cplusplus\n"   \
        "extern \"C\" {\n"       \
        "#endif\n\n"
     
    def addCppSentinelEnd(self): 
        self.buf +=                        \
        "#ifdef __cplusplus\n"             \
        "} //end brace for extern \"C\"\n" \
        "#endif\n"

    def addAppDefines(self):
        self.addDefine("APP_NAME        ", "\""+self.moduleName+"\"")
        self.addDefine("APP_VERSION     ", "\"0.01\"")
        self.addDefine("APP_DESCRIPTION ", "\"\"")
        self.addDefine("APP_AUTHOR      ", "\""+self.conf.author+"\"")
        self.addDefine("APP_LICENSE     ", "\""+self.conf.license+ "\"")
        self.addDefine("APP_ORG         ", "\"\"")
#    addDefine("APP_LOGFILE",     "glib.log")
#    addDefine("APP_PIDFILE",     "/tmp/glibtest.pid")

    def addComment(self, comment):
        self.buf += "  // "+comment+"\n"

    def save(self, dir):
        # Open files to be generated
        try:
            file = open(dir+"/"+self.fileName, 'w')
            file.write(self.buf)
            file.close()
        except IOError:
            logging.debug("Could not open file %s" % (fileName))
            exit()
    
    def addSignal(self, signal, handler):
        self.prototypes += "void "+handler+"(int sig);\n"
        self.code       += "void "+handler+"(int sig) {\n\n}\n\n"
        self.main       += "  signal("+signal+", "+handler+");\n"
    
    def addSignals(self):
        self.addInclude("signal.h")
        self.addSignal("SIGINT", "sigint")
        self.addSignal("SIGHUP", "sighup")
        self.addSignal("SIGUSR1", "sigusr1")
        self.addSignal("SIGUSR2", "sigusr2")
        self.addSignal("SIGTERM", "sigterm")
        
    def addGtk(self):
        #if (conf.gtk):    
        self.addInclude("gtk/gtk.h")
    
    def addQtIncludes(self):    
        self.addInclude("QApplication")
        self.addInclude("QCoreApplication")
        self.addInclude("QMainWindow")
        seld.addInclude("QAction")
        seld.addInclude("QLayout")
        seld.addInclude("QMenu")
        seld.addInclude("QMenuBar")
        seld.addInclude("QStatusBar")
        
        self.addInclude("QPushButton")
        self.addInclude("QLabel")
        seld.addInclude("QLineEdit")
        seld.addInclude("QComboBox")

        self.addInclude("QStatusBar")
        self.addInclude("QTextEdit")
        seld.addInclude("QPlainTextEdit")
        seld.addInclude("QFile")
        seld.addInclude("QFileDialog")
        seld.addInclude("QDialogButtonBox")
        seld.addInclude("QMessageBox")
        
        seld.addInclude("QDataStream")
        seld.addInclude("QSignalMapper")
        seld.addInclude("QMouseEvent")
        seld.addInclude("QDebug")
                                                                                        
        
    def addQt(self):    
        self.addQtIncludes()
        
        self.main += "  Q_INIT_RESOURCE(application);\n\n"
        self.main += "  QApplication app(argc, argv);\n"
        self.main += "  QCoreApplication::setOrganizationName(APP_ORG);\n"
        self.main += "  QCoreApplication::setApplicationName(APP_NAME);\n"
        self.main += "  QCoreApplication::setApplicationVersion(APP_VERSION);\n\n"
#        self.main += "  QCommandLineParser parser;\n"
#        self.main += "  parser.setApplicationDescription(QCoreApplication::applicationName());\n"
#        self.main += "  parser.addHelpOption();\n"
#        self.main += "  parser.addVersionOption();\n"
#        self.main += "  parser.addPositionalArgument("file", "The file to open.");\n"
#        self.main += "  parser.process(app);\n"
        
        self.main += "  MainWindow mainWin;\n"
#        self.main += "  if (!parser.positionalArguments().isEmpty())\n"
#        self.main += "  mainWin.loadFile(parser.positionalArguments().first());\n"
        self.main += "  mainWin.show();\n"
        self.main += "  return app.exec();\n"
                
    def addMain(self):
        self.main = "int main(int argc, char *argv[]) {\n\n" + self.main
        self.main += "  return 0;\n"
        self.main += "}\n"
        
    def addStdIncludes(self):
        if self.isCpp:
            self.addInclude("iostream")
        else:
            self.addInclude("stdio.h")
            self.addInclude("stdlib.h")
            self.addInclude("stdint.h")
            self.addInclude("string.h")
            self.addInclude("unistd.h")
            self.addInclude("sys/types.h")
            self.addInclude("errno.h")
        
    def replace(self, str, newStr):
        self.buf = self.buf.replace(str, newStr)

    def newLine(self):
        self.buf += "\n"
    
    def create(self):
        
        self.addHeader()
        
        if self.conf.main and not self.isHeader:
            self.addStdIncludes()
        
        if self.conf.signals and not self.isHeader:
            self.addSignals()
            
        if self.conf.qt:
            self.addQt()
        
        
        if self.conf.main and self.isHeader:
            self.addAppDefines()

        if self.conf.main and not self.isHeader:
            self.addMain()
            
        if not self.isHeader:
            self.addInclude(self.moduleName+".h", True)

        # Sections
        self.buf = ""
        self.buf = self.buf + self.header
        
        if self.isHeader:
            self.addSentinelBegin(self.moduleName.upper())

        if self.isHeader and not self.isCpp:
            self.addCppSentinel()
        
        self.newLine()
        self.addSection("Includes")
        self.buf += self.include
        
        self.addSection("Macros")
        self.buf += self.defines

        self.addSection("Variables")
        self.buf += self.variables

        self.addSection("Prototypes")
        self.buf += self.prototypes
        
        if not self.isHeader:
            self.addSection("Code")
            self.buf = self.buf + self.code
        
            self.buf += self.main    
            
        if self.isHeader:
            self.addSentinelEnd()
        
        if self.isHeader and not self.isCpp:
            self.addCppSentinelEnd()

        self.replace("__FILENAME__", self.fileName     )
        self.replace("__BRIEF__",    self.conf.brief   )
        self.replace("__DATE__",     self.conf.date    )
        self.replace("__AUTHOR__",   self.conf.author  )    
        self.replace("__LICENSE__",  self.conf.license )
    
    def print(self):
        #self.create()
        print(self.buf)

class CClass(CFile):
    className = ""
    parrent   = ""
    methods   = ""
    classBuf  = ""
    qt        = False
    
    def __init__(self, conf, parrent, isHeader):
        conf.isCpp = True
        super().__init__(conf, isHeader)
        self.className = self.moduleName
        self.parrent   = parrent
        
        
    def addMethod(self, dataType, methodName, arguments):
        if self.isHeader:
            if dataType=="":
                self.classBuf += "    " + methodName+"("+arguments+");\n"
            else:
                self.classBuf += "    " +dataType + " " + methodName+"("+arguments+");\n"
        else:
            self.code += self.className+"::"+methodName+"() {\n"
            self.code += "\n}\n\n"
            
    def create(self):
        
        self.addMethod("", self.className, "")
        self.addMethod("", "~"+self.className, "")

        if self.isHeader:
            if (self.parrent == ""):
                self.prototypes += "class "+self.className+" {\n"
            else:
                self.prototypes += "class "+self.className+": public "+self.parrent+" {\n"
            
            if self.qt:
                self.prototypes += "  Q_OBJECT\n"
            
            self.prototypes += "  public:\n"
            self.prototypes += self.classBuf
            if self.qt:
                self.prototypes += "  private slots:\n"
                
            self.prototypes += "  private:\n"
            self.prototypes += "};\n"
                
        super().create()
            
    def __str__(self):
        return

class QtClass(CClass):
    def __init__(self, conf, isHeader):
        conf.qt = True
        super().__init__(conf, "", isHeader)
      
    def addQtIncludes(self):    
        self.addInclude("QApplication")
        self.addInclude("QCoreApplication")
        self.addInclude("QMainWindow")
        self.addInclude("QAction")
        self.addInclude("QLayout")
        self.addInclude("QMenu")
        self.addInclude("QMenuBar")
        self.addInclude("QStatusBar")
        
        self.addInclude("QPushButton")
        self.addInclude("QLabel")
        self.addInclude("QLineEdit")
        self.addInclude("QComboBox")

        self.addInclude("QStatusBar")
        self.addInclude("QTextEdit")
        self.addInclude("QPlainTextEdit")
        self.addInclude("QFile")
        self.addInclude("QFileDialog")
        self.addInclude("QDialogButtonBox")
        self.addInclude("QMessageBox")
        
        self.addInclude("QDataStream")
        self.addInclude("QSignalMapper")
        self.addInclude("QMouseEvent")
        self.addInclude("QDebug")
        
    def MainWindow(self):
        self.moduleName = "MainWindow"
        self.parrent    = "QMainWindow"
        if not self.isHeader:
            self.addQtIncludes()            
        self.create()
        
    def Dialog(self):
        return

    
def newFile(dir, fileName):
    # Open files to be generated
    try:
        file = open(dir+"/"+fileName, 'w')
        return file
    except IOError:
        logging.debug("Could not open file %s" % (fileName))
        exit()
                                
def textToFile(args, fileName, text):
    file = newFile(args.dir, fileName)
    file.write(text)
    file.close()

def newModule(dir, conf):
    
    # ask for some information
    conf.ask("C/C++ module")
    
    if not conf.main:
        conf.main = query_yn("Add main() function", "no")
    
    if conf.main and not conf.isCpp:
        conf.gtk = query_yn("GTK project", "no")
        conf.signals = query_yn("Include signals", "no")
          
    if conf.main and conf.isCpp:    
        conf.qt = query_yn("Qt project", "no")
    
    fileC = CFile(conf, False)
    fileH = CFile(conf, True)
    
    fileH.create()
    fileC.create()
    
    fileH.save(dir)
    fileC.save(dir)


def newClass(dir, conf):

    # ask for some information
    conf.ask("C++ class")

    fileH = CClass(conf, "", True)
    fileC = CClass(conf, "", False)
    
    fileH.create()
    fileC.create()
    
    fileH.save(dir)
    fileC.save(dir)

def printInfo():
    print("Script name    " + AppName)
    print("Script version " + AppVersion)
    print("Script path    " + os.path.realpath(__file__))

    
# Absolute path to script itself        
scriptPath = os.path.abspath(os.path.dirname(sys.argv[0]))
mpPath     = scriptPath+"/.."    


def cmd_qtmain(args, conf):
    print("qtmain")
    exit(0)   

def cmd_qtwin(args, conf):
    print("qtwin")
    conf.moduleName = "MainWindow"
    qtH = QtClass(conf, True)
    qtC = QtClass(conf, False)
    qtH.MainWindow()
    qtC.MainWindow()
    qtH.print()
    qtC.print()
    
    exit(0)

def cmd_qtdia(args, conf):
    print("qtdia")
    exit(0)

def cmd_newc(args, conf):
    conf.isCpp = False
    newModule(args.dir, conf)
    exit(0)

def cmd_newcpp(args, conf):
    conf.isCpp = True
    newModule(args.dir, conf)
    exit(0)

def cmd_newclass(args, conf):
    newClass(args.dir, conf)    
    exit(0)
        
def cmd_giti(args, conf):
    textToFile(args, ".gitignore", gitIgnore)
    exit(0)

def main():
    
    conf = CConf()
    
    logging.basicConfig(level=logging.DEBUG)

    parrent_parser = argparse.ArgumentParser(add_help=False)         
    parrent_parser.add_argument("--license",  type=str,  help="License of new file",           default=conf.license)
    parrent_parser.add_argument("--author",   type=str,  help="Author of file",                default=conf.name+" <"+conf.email+">")

    parrent_parser.add_argument("--dir",      type=str,  help="Directory where to store file", default=".")
    
    parrent_parser.add_argument("--main",     action="store_true",  help="Include main() function into module", default=False)
    parrent_parser.add_argument("--cpp",      action="store_true",  help="Module is a C++ file", default=False)
    parrent_parser.add_argument("--name",     type=str,  help="Name of C/C++ module", default="")
    parrent_parser.add_argument("--brief",    type=str,  help="Brief description",    default="")
    

    # options parsing
    parser = argparse.ArgumentParser(
             prog=AppName+'.py',
             description="Makeplate C/C++ template generator", 
             epilog = "  ",
             parents = [parrent_parser],
             )
             
    parser.add_argument("--version",  action='version',  help="Directory where to store file", version=AppVersion)
             
    subparsers = parser.add_subparsers(help="")
    parser_newc = subparsers.add_parser("newc",     parents=[parrent_parser],  help="Create a new C and H file set")
    parser_newc.set_defaults(func=cmd_newc)
    parser_newclass = subparsers.add_parser("newclass", parents=[parrent_parser],   help="Create a new C++ class")
    parser_newclass.set_defaults(func=cmd_newclass)
    parser_newcpp = subparsers.add_parser("newcpp", parents=[parrent_parser],  help="Create a new C++ file")
    parser_newcpp.set_defaults(func=cmd_newcpp)
#    parser_qtdia = subparsers.add_parser("qtdia",   parents=[parrent_parser],  help="Create a Qt5 dialog")
#    parser_qtdia.set_defaults(func=cmd_qtdia)
#    parser_qtmain = subparsers.add_parser("qtmain", parents=[parrent_parser],  help="Create a Qt5 main application")
#    parser_qtmain.set_defaults(func=cmd_qtmain)
    parser_qtwin = subparsers.add_parser("qtwin",   parents=[parrent_parser],  help="Create a Qt5 main window")
    parser_qtwin.set_defaults(func=cmd_qtwin)
#    parser_qtdia = subparsers.add_parser("qtdia",   parents=[parrent_parser],  help="Create a Qt5 dialog")
#    parser_qtdia.set_defaults(func=cmd_qtdia)
    parser_qtdia = subparsers.add_parser("giti",    parents=[parrent_parser],  help="Create .gitignore file")
    parser_qtdia.set_defaults(func=cmd_giti)
    
#    parser.add_argument("--header",   type=str,            help="External header file",  default="headerExample")
#    subparsers = parser.add_subparsers(title='subcommands', help="sfda fdsa fdsa afsd")

    args = parser.parse_args()
    if hasattr(args, 'author'):
        conf.author  = args.author
    if hasattr(args, 'license'):
        conf.license = args.license        
    
    if hasattr(args, 'main'):
        conf.main = args.main
    if hasattr(args, 'cpp'):
        conf.isCpp = args.cpp
    if hasattr(args, 'name'):
        conf.moduleName = args.name
    if hasattr(args, 'brief'):
        conf.brief = args.brief

    
    if hasattr(args, 'func'):
        args.func(args, conf)
        exit(0)
    
    parser.print_help()
    exit(0)

def query_list(question, db, default="yes"):
    prompt = " >"

    #print(db)
    while 1:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        print(choice)
        for x in db:
            if (x.lower()==choice):
                return x
            
        print("\nPlease resplond with: ")
        for c in db:
            print("  "+c)
            
    
def query_yn(question, default="yes"):
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)
    
    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")
    
    
headerExample="""/**
 *---------------------------------------------------------------------------
 * @brief    __BRIEF__
 *
 * @file     __FILENAME__
 * @author   __AUTHOR__
 * @date     __DATE__
 * @license  __LICENSE__
 *
 *---------------------------------------------------------------------------
 *
 *
 */
"""    

gtkMainExample="""

int main(int argc, char *argv[]) {
 
    signal(SIGINT, sigInt);
    signal(SIGHUP, sigHup);


// GTK Glade --------------------------------------------------------------------

    gtk_init(&argc, &argv);

    builder = gtk_builder_new();
    gtk_builder_add_from_file (builder, "gtkTest.glade", NULL);

    window = GTK_WIDGET(gtk_builder_get_object(builder, "window2"));
    gtk_builder_connect_signals(builder, NULL);

    //g_object_unref(builder);

    GtkWidget *w;
    GtkTextIter iter;
    w = gtk_builder_get_object(builder, "textview2");
    //gtk_text_view_set_buffer(w, buf);
    buf = gtk_text_view_get_buffer(w);
    gtk_text_buffer_get_iter_at_offset(buf, &iter, 0);
    gtk_text_buffer_insert(buf, &iter, "Kalle", -1);
    
    return 0;
}
"""

glibMainExample="""
"""

mainExample="""
int main(int argc, char *argv[]) {
        
    return 0;
}
"""

qtCoreMainExample="""
int main(int argc, char *argv[]) {
 
    QCoreApplication app(argc, argv);
         
    return app.exec();
}
"""

qtMainExample="""
int main(int argc, char *argv[]) {
 
    QApplication app(argc, argv);
//    MainWindow w;
//    w.show();
         
    return app.exec();
}
"""



gitIgnore="""
#
# Makeplate .gitignore file
#
# 
# 
#


# Makeplate specific files
#--------------------------------------------------------------------
archive
backup
output
personal*.mk

# Temporary files
#--------------------------------------------------------------------
*.tmp
*.old
*.orig
*~

# Revision control
#--------------------------------------------------------------------
.svn
.git

# C/C++
#--------------------------------------------------------------------

# Object files
*.o
*.ko
*.obj
*.elf
*.lo
*.slo

# Symbols etc
*.lst
*.sym
*.map
*.lss

# Precompiled Headers
*.gch
*.pch

# Static Libraries
*.lib
*.a
*.la
*.lo
*.lai

# Shared libraries (inc. Windows DLLs)
*.dll
*.so
*.so.*
*.dylib

# Executables
*.exe
*.out
*.app
*.i*86
*.x86_64
*.hex
*.bin
*.elf
*.a

# Debug files
*.dSYM/

# Makefile specific
#--------------------------------------------------------------------
*.d
.dep


# Qt 
#--------------------------------------------------------------------
*.moc
moc_*.h
moc_*.cpp
*_moc.h
*_moc.cpp
qrc_*.cpp
ui_*.h

# QtCreator Qml
*.qmlproject.user
*.qmlproject.user.*

# QtCtreator CMake
CMakeLists.txt.user*
"""


argTable="""
"""



if __name__ == "__main__":
    try:
        main()
        sys.exit(0)
    except KeyboardInterrupt as e: # Ctrl-C
        raise e
    except SystemExit as e:        # sys.exit()
        raise e
    except Exception as e:
        print('ERROR, UNEXPECTED EXCEPTION')
        print(str(e))
        traceback.print_exc()
        os._exit(1)

        
