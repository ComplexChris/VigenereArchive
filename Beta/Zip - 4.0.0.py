# coding: utf-8


## Container Archive Encryption Program
## Written and Devoloped by Chris J. Nguyen
# rgetroiherihsiyurg


import os, sys, zipfile, StringIO, string, random, shutil, time

__version__ = "4.0.0"
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
_Fancy = "\n\n%s\n\n" % _Bricks
COMP_TYPE = 8
BLOCK = 256

try:
    _ScriptLoc = os.path.dirname(os.path.abspath(__file__))
except NameError:
    _ScriptLoc = os.path.dirname(os.path.abspath(sys.argv[0]))
_LogLoc = os.path.join(_ScriptLoc, 'Log.txt' )
_CacheLoc = os.path.join(_ScriptLoc, '_Cache')
_UsersLoc = os.path.join(_ScriptLoc, '_Users')


class SAK():
    
    ExitCode = "STOP, EXIT, QUIT, FUCK"

    Sleep = lambda self, zzz=1: time.sleep(zzz)
    Exists = lambda self, path: os.path.exists(path)    
    CD = lambda self, path: os.chdir(path) if self.Exists(path) else 0

    def GetDetails(self):
        cwd = os.getcwd()
        sVer = sys.version

        items = [_Fancy, 
                "\nScript Location: %s \nCache Location: %s \nArchive Location: %s " % (_ScriptLoc, _CacheLoc, _UsersLoc),
                 "Current Directory: %s \n\nProgram Version: %s \nSystem Version %s " % (cwd, __version__, sVer),
                 "\nRelease Date: %s Copyright: %s \nAuthor: %s " % (__date__, __copyright__, __author__)
        for line in items: print line
                 
    def Clean(self, Path, verbose=True):
        try:
            if os.path.isdir(Path):
                shutil.rmtree(Path)
            else:
                os.remove(Path)
        except Exception as E:
            if verbose: print '\nUnable to remove file(s)!\nPlease close any open processes!\n', E
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
        Bad = '/\:*?<>"|'
        Bad = string.punctuation
        BaseChars = (string.ascii_letters + string.digits)
        LBS = len(BaseChars)
        out = ''
        for c in String:
            if c not in BaseChars:
                out += BaseChars[ord(c) % LBS ]
            else: out += c
        return out
            
    def GetLogin(self, Confirm=True):
        while True:
            print _Fancy
            UN = self.Smart_Input('Enter User Name >>> ').upper()
            PW = self.Smart_Input('Enter Password >>> ')
            if Confirm:
                PW2 = self.Smart_Input('Confirm Password >>> ')
                if PW == PW2: Confirm=False
                else: print 'Passwords do not match!'
            if Confirm==0:
                return UN, PW
                
    def GetFileName(self, UN, PW):
        DefaultPhrase = self.Vigenere('_CoMpLeXiTy_314', UN)
        P1 = self.Vigenere(DefaultPhrase, UN, True)
        P2 = self.Vigenere(P1, PW, True)
        Name = ''
        for char in P1+P2:
            cInt = self.Collatz( ord(char) * 4 )%256
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

    def Vigenere(self, string, key, encrypt=None):
        #return string
        LP = len(key)
        out = ''; x=0
        los = len(string)
        #block = len( str(los) ) - (1 if los>10 else 0 )
        for x in range( los ):
            val1, val2 = ord( string[x] ), ord( key[x % LP ] )
            if encrypt != None:
                #print "\nUsing Enigma!"
                val3 = val1+val2 if encrypt==False else val1-val2 ## if True else (False)      
            else:   
                a, b = min([val1, val2]), max([val1, val2])
                val3 = val1+val2 if (val2<val1 and val1+val2<256) else b-a
            v3 = val3%256
            out += chr(v3)
        return out
                        
    def VigLarge(self, string, key, encrypt=None, Blocks=512):
        if False: #len(string) < Blocks/2.5:
            print "\nLarge going to straight..."
            return self.Vigenere(string, key, encrypt)
        #print "LOS: ", len(string),
        middle = len(string)/2
        a,b = middle-Blocks, middle+Blocks
        modified = string[:Blocks] + string[-Blocks:]
        viged = self.Vigenere(modified, key, encrypt)
        out = viged[:Blocks] + string[Blocks:-Blocks] + viged[-Blocks:]
        #print middle, a,b
        return out

    def MakeBlocks(self, String, Size):
        ## Creates blocks from string based on "Size"
        x=0; LOS=len(String)
        while x*Size < LOS: #for x in range(1, (len(String) / Size) ) :
            x += 1
            a, b = ((x-1)*Size), (x*Size)
            #print "The X: ", x, "  |\tA, B : ", a, b
            yield String[ a : b ]
                
    def VigBlocks(self, String, PW, mode=True, Size=2**15, Path=None):
        ## Encrypts blocks for large strings
        if False: #len(String) < 2**20 :
            print "\nBlocks going to large..."
            return self.VigLarge(String, PW, mode, Size)
        LOS = len(String)
        #Tools.WriteFile(Path, '')
        x=-1
        mass = ''
        for part in self.MakeBlocks(String, Size):
            x+=1
            #frag = String[ (x-1)*BlockSize : x*BlockSize ]
            if x % 2 == 0:
                chunk = Tools.VigLarge(part, PW, mode, Size/8) # Tools.VigLarge( part, PW, mode, cap )
            else:
                chunk = part
            mass += chunk
            #Tools.WriteFile(Path, chunk, "ab")
        return mass

    def AutoVig(self, string, key, encrypt=None, Blocks=512):
        LOS = len(string)
        if LOS > 2**20:
            print "\nUsing Blocks"
            product = self.VigBlocks(string, key, encrypt, 2048)
        elif LOS > 2**15:
            print "\nUsing Large"
            product = self.VigLarge(string, key, encrypt, 512)
        else:
            print "\nUsing Regular"
            product = self.Vigenere(string, key, encrypt)
            #product = self.Vig(string, key, encrypt, limit=2056, Blocks=512)[0]
        return product
        
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
        ## Creates archive file in local directory
        FileInst = StringIO.StringIO() 
        with zipfile.ZipFile( FileInst, mode='w', compression=COMP_TYPE ) as ZipF:
            ZipF.writestr('MyPasswords.txt', 'Facebook = "Bob1992" ')
            ZipF.writestr('MyNotes.txt', 'To do: Decrypt Russian Nuclear Launch Codes "XMG-01 (WMD)" ')
            ZipF.close()
        Encrypted = Tools.AutoVig( FileInst.getvalue(), Password, True, BLOCK)
        Tools.WriteFile(ZipName, Encrypted )
                
    def OpenZip(self, ZipName, Password):
        ## Opens and decrypts zip file and returns decrypted zip file instance
        raw_zip = Tools.ReadFile(ZipName)
        Decrypted = Tools.AutoVig(raw_zip, Password, False, BLOCK)
        buff = StringIO.StringIO(Decrypted)
        if zipfile.is_zipfile( buff ):
            print "\nOpening Archive..."
            ZipInst = zipfile.ZipFile( buff, 'r', compression=COMP_TYPE )
            return ZipInst
        else: return False  
        
    def WriteZip(self, TmpDir, Password=None, Destination=None):
        ## Reads all content of temp directory 
        ## and writes to zip IO instance
        FileInst = StringIO.StringIO()
        with zipfile.ZipFile( FileInst, mode='w', compression=COMP_TYPE ) as ZipInst:
            for raw_file in self.WalkDir( TmpDir ):
                ZipInst.write( raw_file, os.path.relpath(raw_file, TmpDir) ) # os.path.join(root, raw_file))
        if (Destination and Password) != (None, None):
            Path = os.path.join(_ScriptLoc, Destination)
            Encrypt = Tools.AutoVig(FileInst.getvalue(), Password, True, BLOCK)
            Tools.WriteFile(Path, Encrypt)

    def Decompress(self, ZipInst, ToDir = None ):
        #Extracts all files in decrypted Zip IO instance
        Tools.Log (str("Decompressing: "+ToDir))
        if ToDir==None: ToDir = self.ToDir
        ZipInst.extractall( ToDir )
        
class User(ArcZip):
    
    def __init__(self, Active=True):
        if Active:
            Tools.CD(_ScriptLoc)
            if Tools.Exists(_CacheLoc):
                Tools.Clean (_CacheLoc)
            if Tools.Exists(_CacheLoc)==False:
                os.mkdir(_CacheLoc)
            if Tools.Exists(_UsersLoc)==False:
                os.mkdir(_UsersLoc)

            self.Username, self.Password = '', ''
            self.ZipName, self.ZipInst = '', None
            self.Start()
    
    def Depart(self, Cleanup=True, verbose=True):
        print _Fancy, '\nGoodBye!' if verbose else ""
        shutil.rmtree(_CacheLoc)
        sys.exit()
        ## Delete Tmp Dir...
    
    def UpdateUserVar(self, Switch):    
        self.Username, self.Password = Tools.GetLogin( Switch ) #'CHRIS', 'ares'
        Name = Tools.MakeASCII(Tools.GetFileName(self.Username, self.Password) )[:20]+'.ADF'
        self.ZipName = os.path.join( _ScriptLoc, "_Users", Name)
        RawDir = Name.rstrip('.ADF')
        self.ToDir = os.path.join(_ScriptLoc, '_Cache', ".$"+RawDir) ##'.$'
            
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
                        else: print "\nUnable to proccess archive!" 
                        
                    else:
                        print "\nAccount not found!"
                else:
                    if True: #ArcStat==0:
                        self.CreateZip(self.ZipName, self.Password)
                        print "\nAccount created successfully! \nPlease re-login to continue!"
                    else: 
                        print "\nArchive already exists. Please log in instead."
                
    def Run(self):
        Menu1 = "a. Start Archive \tb. Save Archive \nc. More \t\td. Logout"
        Menu2 = "a. Clear Cache \tb. Delete Archive \nc. Info \t\td. Back
        Msg, Options = "(A/B/C/D)", "ABCD"
        Update = True; MainMenu = True
        print _Fancy, "\nWelcome %s!" % self.Username.title() 
        while True:
            Tools.Sleep(2)
            print _Fancy, Menu1
            Choice = Tools.Raw_Choice(Msg, Options)
            if MainMenu == True:
                if Choice=="C": MainMenu=False
                else: self.MainMenu(Choice, Update)
            else:
                if Choice=="D": MainMenu=True
                self.ExtendedMenu(Choice, Update)

    def ExtendedMenu(self, Choice, Update):
        if Choice == "A":
            for x in range(100):
                Tools.Clean( _CacheLoc, False )
                if Tools.Exists(_CacheLoc)==0: break
        elif Choice == "B":
            self.RemoveArchive()
        elif Choice=="C":
            Tools.GetDetails()

    def MainMenu(self, Choice, Update):
        if Choice == 'A':
            if Update:
                Update=False
                self.ZipInst = self.OpenZip(self.ZipName, self.Password)
            self.StartArchive()
        elif Choice == 'B':
            self.SaveArchive()
            
        elif Choice=='C':
            print "\nComing soon..."
        else:
            if Tools.Exists(self.ToDir) and Update==False:
                print "\nWarning! Did you want to save your archive first?"
                if Tools.Raw_Choice() == "Y": self.SaveArchive()
            raise StandardError

    def RemoveArchive(self):
        print "\nConfirm removale of entire archive by entering the Captcha:"
        code = Tools.RandomString(6, False)
        attempt = raw_input("@#!>%s<?*@ \n> " % code)
        if attempt==code:
            print "\nNow re-login: "
            a, b = Tools.GetLogin(False)
            if (a,b) == (self.Username, self.Password):
                stat = Tools.Clean(self.ZipName)
                if stat != False:
                    print "\nArchive has been removed!"
                else:
                    print "\nUnable to remove archive at this time!"


    def StartArchive(self):
        if Tools.Exists(self.ToDir):
            print "\nAn archive is already started. Please Save or manually remove direcory: \n%s " % self.ToDir
        else:
            self.Decompress(self.ZipInst, self.ToDir)
            print "\nArchive has been opened at: \n%s " % (self.ToDir)
            
            try: os.startfile(self.ToDir)
            except: pass
    def SaveArchive(self):
        if Tools.Exists(self.ToDir) and Update==False:
            print '\nSaving...'
            Update=True
            ZipInstByte = self.WriteZip(self.ToDir, self.Password, self.ZipName )
            RmStat = Tools.Clean( self.ToDir )
            print "\nArchive has been saved!"
            print "...and the temporary directory %s removed" % ("WAS" if RmStat!=False else "WAS NOT") 
            print "Location: ", os.path.relpath( self.ToDir )
            
        else:
            print "\nArchive not started! \nNo changes made to archive!"
                
if __name__=="__main__":
    while True:
        try:
            c = User()
        except StandardError:
            pass
        except SystemExit:
            print "\nGoodBye!!!"
            break
