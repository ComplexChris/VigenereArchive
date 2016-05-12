# coding: utf-8

import os, sys, zipfile, StringIO, string, random, shutil, time

__version__ = "2.2.1"
__author__ = "Chris J. Nguyen"
__date__ = "April 6th, 2016"
__copyright__ = "(C) 2016-2018 Chris J. Nguyen. GNU GPL 3."
## freeNote.net
## irc
## filename encryption python

tmp_s = 'There he was...'
tmp_k = 'password'
#TmpZip = zipfile.ZipFile('Test.zip', 'w')

_Bricks = "~-"*16
_Fancy = "\n\n\n%s\n\n" % _Bricks


def test():
    FileInst = StringIO.StringIO() 
    with zipfile.ZipFile( FileInst, mode='w' ) as ZipF:
        #for raw_file in WalkDir( TmpDir ):
        ZipF.writestr('MyPasswords.txt', 'Facebook = "Bob1992" ')
        ZipF.writestr('MyNotes.txt', 'To do: Decrypt Russian Nuclear Launch Codes "XMG-01 (WMD)" ')
        ZipF.close()                     
    return FileInst

try:
    _ScriptLoc = os.path.dirname(os.path.abspath(__file__))
except NameError:
    _ScriptLoc = os.path.dirname(os.path.abspath(sys.argv[0]))
_LogLoc = os.path.join(_ScriptLoc, 'Log.txt' )
_CacheLoc = os.path.join(_ScriptLoc, '_Cache')


class SAK():
    
    ExitCode = "STOP, EXIT, QUIT, FUCK"

    Sleep = lambda self, zzz=1: time.sleep(zzz)
    Exists = lambda self, path: os.path.exists(path)    
    CD = lambda self, path: os.chdir(path) if self.Exists(path) else 0
    
    def Clean(self, Directory):
        try:
            shutil.rmtree(Directory)
        except Exception as E:
            print '\nUnable to remove directory!\nPlease close any open processes!\n', E
            return False
            
    def Log(self, Stat, LogName= _LogLoc ):
        self.WriteFile(LogName, '\n\n'+Stat, 'a')
                
    def ReadFile(self, FileName, mode='rb'):
        with file(FileName, mode) as f:
            return f.read()
            
    def WriteFile(self, FileName, Content, mode='wb'):
        with file(FileName, mode) as f:
            f.write(Content)
        f.close()
        
    def RandomString(self, length=10, CanExist=False ):
        BaseChars = (string.ascii_letters + string.digits) * random.randint(4,8)
        while True:
            Out = ''.join( random.sample( BaseChars, random.randint(8,16) ) )
            if self.Exists(Out) == CanExist:
                return '_'+Out
                
    def Smart_Input(self, msg='(Y/N)'):
        Out = raw_input(msg)
        if Out.upper() in self.ExitCode and len(Out)==4:
            sys.exit()
        else:
            return Out
            
    def Raw_Choice(self, Msg='(Y/N)', Options='YN', Length=1):
        while True:
            Answer = self.Smart_Input(Msg+'> ').upper()
            if Answer in Options and len(Answer)==Length:
                return Answer
                
    def MakeASCII(self, String):
        ## Filters out primary characters
        BaseChars = (string.ascii_letters + string.digits)
        out = ''
        for c in String:
            if c in BaseChars:
                out += c
        return out
            
    def GetLogin(self, Confirm=True):
        while True:
            UN = self.Smart_Input('Enter User Name >>> ').upper()
            PW = self.Smart_Input('Enter Password >>> ')
            if Confirm:
                PW2 = self.Smart_Input('Confirm Password >>> ')
                if PW == PW2: Confirm=False
                else: print 'Passwords do not match!'
            if Confirm==0:
                return UN, PW
                
    def GetFileName(self, UN, PW):
        DefaultPhrase = self.Vig('_CoMpLeXiTy_314_Alpha_', UN)
        P1 = self.Vig(DefaultPhrase, UN, True)
        P2 = self.Vig(P1, PW, True)
        Name = ''
        for char in P1[0]+P2[0]:
            cInt = self.Collatz( ord(char) *4 )%256
            Name += chr( cInt ) if cInt>0 else ''
        return Name #(Name, P1, P2)
        
    def Collatz(self, n):
    ## Basic algorithm
        n = abs(n); numb=[]
        if n<=2: return n
        while n!=1:
            numb.append(n)
            if n%2==0 and n!=0: n/=2
            else: n=(n*3)+1
        return max(numb)
        
    def Vig(self, strings, key, encrypt=None, limit=2056):
        ## Vigenere Function accepts multiple strings
        ## Allows 3 different encryption "modes"
        ## Finalized April 9th, 2016

        products = []
        LP = len(key)
        string_type = type( strings )   
        if string_type not in (list, tuple): 
            if string_type == str:
                strings = [strings]
            else:
                raise TypeError
        if '' in (strings, key): return [strings]       
        for string in strings :
            
            if False: #len(string)>limit:
                print "\nApplying Smart Engine..\n"
                ORG = string
                middle = len(string)/2
                a,b = middle-512, middle+512
                modified = string[:512] + string[-512:]
                out = self.Vig(modified, key, encrypt, limit) [0]
                out = out[:512] + string[512:-512] + out[-512:]
            else:
                out = '';
                for x in range( len(string) ):
                    val1, val2 = ord( string[x] ), ord( key[x % LP ] )
                    if encrypt != None:
                        val3 = val1+val2 if encrypt else val1-val2 ## if True else (False)      
                    else:   
                        a, b = min([val1, val2]), max([val1, val2])
                        val3 = val1+val2 if (val2<val1 and val1+val2<256) else b-a
                    v3 = val3%256
                    out += chr(v3) # if v3>0 else ''
            products.append( out )      
        return products 
            
Tools = SAK()


class ArcZip():
    
    def __init__(self, Active=True):
        pass
        
    def WalkDir(self, path):
        ## Generator object for directory walks
        for root, dirs, files in os.walk(path):
            for f in files:
                yield os.path.join(root, f)
                
    def CreateZip(self, ZipName, Password):
        global FileInst
        ## Creates archive file in local directory
        FileInst = StringIO.StringIO() 
        with zipfile.ZipFile( FileInst, mode='w' ) as ZipF:
            #for raw_file in WalkDir( TmpDir ):
            ZipF.writestr('MyPasswords.txt', 'Facebook = "Bob1992" ')
            ZipF.writestr('MyNotes.txt', 'To do: Decrypt Russian Nuclear Launch Codes "XMG-01 (WMD)" ')
            ZipF.close()
        #print FileInst.getvalue()
        Tools.WriteFile(ZipName, Tools.Vig(FileInst.getvalue(),Password,True)[0] )
                
    def OpenZip(self, ZipName, Password):
        global buff, ZipInst
        ## Opens and decrypts zip file and returns decrypted zip file instance
        raw_zip = Tools.ReadFile(ZipName)
        Decrypted = Tools.Vig(raw_zip, Password, 0)[0]
        buff = StringIO.StringIO(Decrypted)
        if zipfile.is_zipfile( buff ): 
            ZipInst = zipfile.ZipFile( buff )
            return ZipInst
        else: return False  
        
    def WriteZip(self, TmpDir, Password=None, Destination=None):
        ## Reads all content of temp directory 
        ## and writes to zip IO instance
        FileInst = StringIO.StringIO() 
        with zipfile.ZipFile( FileInst, mode='w' ) as ZipInst:
            for raw_file in self.WalkDir( TmpDir ):
                ZipInst.write( raw_file, os.path.relpath(raw_file, TmpDir) ) # os.path.join(root, raw_file))
        if (Destination and Password) != (None, None): 
            Encrypt = Tools.Vig(FileInst.getvalue(), Password, True)[0]
            Tools.WriteFile(os.path.join(_ScriptLoc, Destination), Encrypt)

    def Decompress(self, ZipInst, ToDir = None ):
        Tools.Log (str("Decompressing: "+ToDir))
        if ToDir==None: ToDir = self.ToDir
        ZipInst.extractall( ToDir )
        
class User(ArcZip):
    
    def __init__(self, Active=True):
        if Active:
            Tools.CD(_ScriptLoc)
            Tools.Clean( _CacheLoc )
            if Tools.Exists(_CacheLoc) == False:
                os.mkdir('_Cache')

            self.Username, self.Password = '', ''
            self.ZipName, self.ZipInst = '', None
            self.Start()
    
    def Depart(self, Cleanup=True):
        print '\nGoodBye!', _Fancy
        shutil.rmtree(_CacheLoc)
        sys.exit()
        ## Delete Tmp Dir...
    
    def UpdateUserVar(self, Switch):    
        self.Username, self.Password = 'CHRIS', 'ares' # Tools.GetLogin( Switch )
        Name = Tools.MakeASCII(Tools.GetFileName(self.Username, self.Password) ) +'.zip'
        self.ZipName = os.path.join( _ScriptLoc, Name)
        RawDir = Name.rstrip('.zip')
        self.ToDir = os.path.join(_ScriptLoc, '_Cache', RawDir) ##'.$'
            
    def Start(self):
        Menu = "a. Log in \t\tb. Create Account \nc. Exit"
        while True:
            Tools.Sleep(1.5)
            print _Fancy, Menu
            Choice = Tools.Raw_Choice('(A/B/C)', 'ABC')
            
            if Choice=='C': self.Depart()
            else:
                ## Complex method of assigning boolean values (Encrypt, Decrypt)
                Either = False if Choice=='A' else True             
                
                self.UpdateUserVar(Either)
                ArcStat = Tools.Exists(self.ZipName)
                if Either==False:
                    if ArcStat:
                        self.ZipInst = self.OpenZip(self.ZipName, self.Password )
                        if self.ZipInst != False: self.Run()
                        else: print "Unable to proccess archive!" 
                        
                    else:
                        print "Account not found!"
                else:
                    if ArcStat==0:
                        self.CreateZip(self.ZipName, self.Password)
                        print "Account created successfully! \nPlease re-login to continue!"
                    else: 
                        print "\nArchive already exists. Please log in instead."
                
    def Run(self):
        Menu1 = "a. Start Archive \tb. Save Archive \nc. More \t\td. Logout"
        Menu2 = ""
        Msg, Options = "(A/B/C/D)", "ABCD"
        Update = True
        print _Fancy, "Welcome %s!" % self.Username.title() 
        while True:
            Tools.Sleep(2)
            if Update:
                Update=False
                Tools.CD(_ScriptLoc)
                self.ZipInst = self.OpenZip(self.ZipName, self.Password)

            print _Fancy, Menu1
            Choice = Tools.Raw_Choice(Msg, Options)
            
            if Choice == 'A':
                if Tools.Exists(self.ToDir):
                    print "\nAn archive is already started. Please Save or manually remove direcory: \n%s " % self.ToDir
                    continue
                else:
                    self.Decompress(self.ZipInst, self.ToDir)
                    print "\nArchive has been opened at: \n%s " % (self.ToDir)
                    
                    try: os.startfile(self.ToDir)
                    except: continue
                
            elif Choice == 'B':
                if Tools.Exists(self.ToDir):
                    print '\nSaving...'
                    Update=True
                    ZipInstByte = self.WriteZip(self.ToDir, self.Password, self.ZipName )
                    RmStat = Tools.Clean( self.ToDir )
                    print "\nArchive has been saved!"
                    print "...and the temporary directory %s removed" % ("WAS" if RmStat!=False else "WAS NOT") 
                    print "Location: ", os.path.relpath( self.ToDir )
                    
                else:
                    print "\nArchive not started! \nNo changes made to archive!"
            elif Choice=='C':
                print "\nComing soon..."
            else:
                self.__init__()
                return
                
if __name__=="__main__":
    c = User()
