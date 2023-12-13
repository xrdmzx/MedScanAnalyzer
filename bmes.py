# by Ahmet Sacan.
# This class contains functions for some cross-platform setup & configuration
# needed in some of my courses.
# See the README.txt file for instructions on making this file available in python.
# imports and Utility functions

import sys,os
#from venv import create   #TODO: is this required? it is not available in python2. If not required, remove it.

class bmes:
    PROJECTNAME=None  #used for projdatadir()
    CUSTOMDATADIR=None  #datadir() will return a default datadir,if you are not happy with that, set this variable.
    CUSTOMDBFILE=None  #dbfile() will return a default file, if you are not happy with that, set this variable.
    CUSTOMTEMPDIR=None
    CUSTOMPATH=None
    db=None #we'll store the database connection here.

def selfdir():
    import os;
    return os.path.dirname(os.path.abspath(__file__));

def ispc():
	if not hasattr(ispc, 'ret'):
		import platform
		sys=platform.system();
		ispc.ret = sys=='Windows' or sys.startswith('CYGWIN')
	return ispc.ret;

def iscolab():
     try:
        import google.colab
        return True
     except:
        return False

#add a Google Drive folder to the path so we can import py files that are in there:
def colab_addpath(folder):
    from google.colab import drive; drive.mount('/content/gdrive');
    import sys; sys.path.append('/content/gdrive/MyDrive/'+folder)

def computername():
	import socket
	return socket.gethostname()

def iscomputername(name):
	return computername().lower() == name.lower()

def iscomputernameprefix(name):
	return computername().lower().startswith(name.lower())

def mkdirif(dir):
	if not os.path.isdir(dir): os.mkdir(dir, 0o777 )
def mkfiledirif(file):
    mkdirif(os.path.dirname(file));

def isfile(file):
    return os.path.isfile(file)

def isfileandnotempty(file):
    return os.path.isfile(file) and os.stat(file).st_size != 0

def filemissingorempty(file):
    return not isfileandnotempty(file)

def isfolder(folder):
    return os.path.isdir(folder)

def isfolderandnotempty(folder):
    return os.path.isdir(folder) and len(os.listdir(folder))!=0

def username():
    import getpass
    return getpass.getuser()

def userhomedir():
    try:
        from pathlib import Path
        return str(Path.home())
    except Exception:
        import os;
        return os.path.expanduser( '~' )

def userdownloaddir():
    return userhomedir()+'/Downloads'
    
def tempdir():
	if bmes.CUSTOMTEMPDIR: return bmes.CUSTOMTEMPDIR;
	import tempfile
	ret=tempfile.gettempdir().replace("\\","/")+'/bmes';
	mkdirif(ret);
	return ret;

def selfdir():
    return selfdir.ret
selfdir.ret = os.path.dirname(os.path.abspath(__file__))

# datadir() gets the default datadir.
# if you want to use your own datadir, set bmes.CUSTOMDATADIR='/my/own/dir'
def datadir():
	if bmes.CUSTOMDATADIR: return bmes.CUSTOMDATADIR;
	if not hasattr(datadir, 'ret'): datadir.ret='';
	ret=datadir.ret;
	if not ret:
		if ispc() and isfolder('c:/data/temp'): ret='c:/data/temp/bmes';
		else: ret=userhomedir()+'/bmes';
		mkdirif(ret)
		datadir.ret=ret;
	return ret;


def trycustomdatadirs( dirs ):
    #only try customdatadirs if bmes::$CUSTOMDATADIR is not set elsewhere.
    if not bmes.CUSTOMDATADIR:
        for x in dirs:
            if os.path.isdir(x):
                bmes.CUSTOMDATADIR=x;
                break;

def projdatadir():
    if bmes.PROJECTNAME: subdir=bmes.PROJECTNAME
    else:
         #subdir=os.path.basename(os.path.dirname(selfdir()))+'_'+os.path.basename(selfdir())
         raise Exception('You must set bmes.PROJECTNAME before you can use projdatadir().');
    out=datadir() + '/' + subdir;
    mkdirif(out);
    return out;


def dbfile():
    if bmes.CUSTOMDBFILE: return bmes.CUSTOMDBFILE
    return datadir()+'/db.sqlite';
    #return selfdir()+'/db.sqlite';

def trycustomdbfiles( dirs ):
    #only try customdatadirs if bmes::$CUSTOMDBFILE is not set elsewhere.
    if not bmes.CUSTOMDBFILE:
        for x in dirs:
            if os.path.isfile(x):
                bmes.CUSTOMDBFILE=x;
                break;

def binpath():
    if bmes.CUSTOMPATH: return bmes.CUSTOMPATH
    #return datadir()+'/db.sqlite';
    return selfdir()+'/bin/geckodriver';

def trycustompath( dirs ):
    #only try customdatadirs if bmes::$CUSTOMPATH is not set elsewhere.
    if not bmes.CUSTOMPATH:
        for x in dirs:
            if os.path.isfile(x):
                bmes.CUSTOMPATH=x;
                break;


def testdb():
    import sqlite3
    if not bmes.db:
        bmes.db=sqlite3.connect('test.sqlite');
    return bmes.db;

def gettempfile(filename=None):
    if filename:
        out=tempdir() + '/' + filename;
        if not isfile(out): return out;
    import tempfile
    suffix=None;
    if filename: suffix='_'+filename;
    tf = tempfile.NamedTemporaryFile(suffix=suffix)
    tf.close()
    out=tf.name;
    return out

def sanitizefilename(file):
    #https://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename
    import string
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    file = ''.join(c for c in file if c in valid_chars)
    if not file: file='noname'
    return file


def downloadurl(url,file='',overwrite=False):
    #%if url is not a remote address, assume it is a local file.
    if not (url.startswith('http://') or url.startswith('https://') or url.startswith('ftp://')):
        if not file:
            file=url
            return file
        if not overwrite:
            import os
            if isfileandnotempty(file): return file;
            import shutil;
            shutil.copyfile(url,file);
            return file;

    if not file:
        file=userdownloaddir() + '/' + sanitizefilename(url.split("?")[0].split("/")[-1])
    elif file.endswith('/'):
        file=file + '/' + sanitizefilename(url)

    
    if isfileandnotempty(file): return file;

    file=file.replace('\\','/').replace('//','/');

    if not ('/' in file):
        file=userdownloaddir() + '/' + file
        if isfileandnotempty(file): return file;
        file=file.replace('\\','/').replace('//','/');


    print('--- NOTICE: Attempting to download & save url [ %s ] to file [ %s ] ...\n'%(url,file));
    import sys
    if (sys.version_info > (3, 0)):
        import ssl
        ssl._create_default_https_context = ssl._create_unverified_context        
        import urllib.request
        urllib.request.urlretrieve(url, file)
    else:
        import urllib
        urllib.urlretrieve(url,file)
    return file

def downloadfile(path):
    print('Obsolete function bmes.downloadfile(). Just use bmes.downloadurl() instead.')
    """If path is a URL, download it to a temp file and return the filename
    Otherwise, assume path is a filename and return as is.
    """
    return downloadurl(path)


#cur should be a database cursor that you already created.
#e.g.: isdbtable(cur, 'students')
def isdbtable(cur,tablename):
	if type(cur).__name__ == 'Connection': cur=cur.cursor()
	return len(cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='"+tablename+"'").fetchall())!=0

def fileread(file):
    #from pathlib import Path
    #return(Path(file).read_text())
    with open(file,'r') as f: return(f.read())

#if stderrfile is not given, we redirect to a temporary file and then print it.
def system_redirecttofile(cmd,stdoutfile=None,stderrfile=None):
    if cmd is list: raise Exception('Only string cmd is supported here.');
    printstdout=False;
    printstderr=False;
    if stdoutfile:
        if not stderrfile:
            printstderr=True;
            stderrfile=gettempfile();
        cmd = cmd +  ' > "' + stdoutfile + '" 2>"' + stderrfile +'"';
    else:
        printstdout=True;
        stdoutfile=gettempfile();
        if stderrfile:
            cmd = cmd +  ' > "' + stdoutfile + '" 2>"' + stderrfile +'"';
        else:
            cmd = cmd +  ' > "' + stdoutfile + '" 2>&1';

    print('Executing command: ' + cmd)
    import os
    os.system(cmd)
    if printstdout:
        with open(stdoutfile,'r') as f: print(f.read())
        os.remove(stdoutfile);
    if printstderr:
        with open(stderrfile,'r') as f: print(f.read())
        os.remove(stderrfile);

def str_spaced(a):
     if isinstance(a,str): return a
     return ' '.join(a)

#similar to matlab's system() call, with a few additional conveniences
def system(cmd,doprint=True,decode=True):
    import subprocess
    if doprint: print("Executing command: " + str_spaced(cmd));
    try: out=subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e: out=e.output;
    if decode: out=out.decode('utf-8','backslashreplace')
    if doprint and out: print(out);
    return out;

#run a command in the background.
def system_bg(cmd,doprint=True):
    import subprocess
    if doprint: print("Executing command in background: " + str_spaced(cmd));
    subprocess.Popen(cmd);

def tryimportingpackage(importname,version=None):
    import importlib
    try: importlib.import_module(importname)
    except Exception as e:
        if isinstance(e, ImportError): return False
        print('--- NOTICE: The package seems installed and importable; but I received the following error message during import: \n'+str(e))
        # because import failed here, the package won't be available in sys.modules[importname], so we won't be able to determine the installed package name.
    import sys
    if version is not None and  version != sys.modules[importname].__version__: return False
    return True
def ispackageinstalled(importname,version=None):
    return tryimportingpackage(importname,version)

#sys.executable sometimes does not work correctly.
def pythonexe():
    import sys
    out=sys.executable;
    if isfile(out): return out;
    import shutil
    out=shutil.which('python')
    if out is not None: return out;
    raise Exception('Cannot locate the python executable.');


# In most cases, importname and packagename are identical.
# Provide both when they are diferent.
# e.g., pipinstall('numpy')
# e.g., pipinstall('Bio', 'biopython')
#if packagename is a list or dictionary, importname is ignored.
#if packagename is a dictionary, it should be in the form of {importname:packagename}.
def installpackage(packagename,importname=None,reinstall=False,method='pip',condaargs=[]):
    if type(packagename) is str and ',' in packagename:
        packagename=packagename.split(',')
    if type(packagename) is list:
        for item in packagename: installpackage(item,None,reinstall,method);
        return
    if type(packagename) is dict:
        for key,item in packagename.items(): installpackage(item,key,reinstall,method);
        return

    if not importname:
        #support version specification, e.g., 'gseapy==1.0.4'
        if '==' in packagename: importname=packagename[:packagename.index('==')];
        else: importname=packagename;

    version=None
    if '==' in packagename: version=packagename[packagename.index('==')+2:];

    isinstalled=ispackageinstalled(importname)
    if isinstalled and not reinstall and version is not None and not ispackageinstalled(importname,version):
         print('Currently installed package ['+importname+'] version is different than the requested version ['+version+']. Re-installing...')
         reinstall=True
        
    if reinstall and isinstalled:
        uninstallpackage(packagename,False,method)
    if reinstall or not isinstalled:
        print('Installing [%s] (importname=%s) using [%s] ...'%(packagename,importname,method));
        if method=='pip':
            cmd=[pythonexe(), '-m','pip','install','-U',packagename];
            #import os;
            #os.system(cmd)
            s=system(cmd)
            if 'ERROR: Could not install packages' in str(s) and 'Consider using the `--user` option' in str(s):
                cmd=[pythonexe(),'-m','pip','install','--user','-U',packagename];
                system(cmd)
        elif method=='conda':
            if tryimportingpackage('conda.cli'):
                import conda.cli
                conda.cli.main('install',  '-y', packagename,*condaargs)
                #adapted from: https://stackoverflow.com/questions/41767340/using-conda-install-within-a-python-script
                #import conda.cli.python_api as Conda
                # The below is roughly equivalent to:
                #  conda install -y 'args-go-here' 'no-whitespace-splitting-occurs' 'square-brackets-optional'
                if False:
                    (stdout_str, stderr_str, return_code_int) = Conda.run_command(
                        Conda.Commands.INSTALL, # alternatively, you can just say "install"
                                # ...it's probably safer long-term to use the Commands class though
                                # Commands include:
                                #  CLEAN,CONFIG,CREATE,INFO,INSTALL,HELP,LIST,REMOVE,SEARCH,UPDATE,RUN
                            #condaargs + [ 'no-whitespace-splitting-occurs', 'square-brackets-optional' ],
                            condaargs,
                            use_exception_handler=True,  # Defaults to False, use that if you want to handle your own exceptions
                            stdout=sys.stdout, # Defaults to being returned as a str (stdout_str)
                            stderr=sys.stderr, # Also defaults to being returned as str (stderr_str)
                            search_path=Conda.SEARCH_PATH  # this is the default; adding only for illustrative purposes
                        )
        else: raise Exception('method should be one of pip|conda');
        if not tryimportingpackage(importname):
            print('FAILED to install package [' + packagename + '], importname [' + importname + ']');
            if method=='conda':
                print('Try installing the package with Anaconda Prompt. Try running the following:');
                print('conda update --all --yes')


#use importname=False to uninstall without checking if it is already installed.
def uninstallpackage(packagename,importname=None,method='pip'):
    #packagename should not have ==versionnumber when doing an uninstall.
    if '==' in packagename: packagename=packagename[:packagename.index('==')];
    if importname is not False:
        if not importname: importname=packagename;
        isinstalled=ispackageinstalled(importname)
    if importname is False or isinstalled:
        print('Un-installing [%s] (importname=%s) using [%s] ...'%(packagename,importname,method));
        if method=='pip':
            system([pythonexe(),'-m','pip','uninstall','-y',packagename])
        elif method=='conda':
             pass
        else: raise Exception('method should be one of pip|conda');
     
def pipinstall(packagename,importname=None,reinstall=False): return installpackage(packagename,importname,reinstall,method='pip');
def condainstall(packagename,importname=None,reinstall=False,condaargs=[]): return installpackage(packagename,importname,reinstall,method='conda',condaargs=condaargs);
def pipuninstall(packagename,importname=None): return uninstallpackage(packagename,importname,method='pip');
def condauninstall(packagename,importname=None): return uninstallpackage(packagename,importname,method='conda');
pipinstall('pillow')