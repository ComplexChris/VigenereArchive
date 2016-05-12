# coding: utf-8 


## Container Archive Encryption Program
## Written and Devoloped by Chris J. Nguyen


import os, sys, zipfile, StringIO, string, random, shutil, time

__version__ = "4.4.3"
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

FAQ = """
Q: How do I add my own document to my Archive? \nA: Cut/Move a file from your computer and paste it into the temporary \ndirectory that is opened when you "Start" your archive in the Main Menu!
\nQ: How do I Quit the program? \nA: Simpily input the corresponding option relating to "Exit" or "Logout" or \njust type "EXIT" when promted to input text!
\nQ: How do I thank or ask the Devolopers? \nA: Email him at: ChrisNguyen180@gmail.com!
\nQ: What type of files may I import to my archive? \nA: Any file less than a GB. As the archive uses a high compression \nratio which may take a couple seconds per MB!
\nQ: How long did it take to make this program? \nA: Apx <1 Month.
\nQ: How many lines of code is this program? \nA: About 500 lines.
\nQ: What are other acceptable inputs? \nA: "LS" or "DIR", "PWD", "FAQ" or "HELP", \n"START" or "OPEN", "CD" followed by a path
\nQ: Is a Dolpin really a mammal? \nA: Yes. They're warm blooded and breath using \ntheir lungs!
\nQ: Wow, fun facts, too? What doesn't this program have? \nA: An espresso bar. :'-( """

DEFAULTS = {
'MyPasswords.txt': 'Facebook = "Bob1992" ',
'MyNotes.txt': 'To do: Decrypt Russian Nuclear Launch Codes "XMG-01 (WMD)" ',
"FAQ.txt": FAQ}


class SAK():
    """ Class of basic extended system functions """
    ExitCode = "STOP, EXIT, QUIT, FUCK"

    Sleep = lambda self, zzz=1: time.sleep(zzz)
    Exists = lambda self, path: os.path.exists(path)
    #GetSize = lambda self, path: os.path.getsize(path)
    CD = lambda self, path: os.chdir(path) if self.Exists(path) else 0

    def MakePath(self, path):
        """Recursively creates path working
        back from the parent directory each iteration"""
        while True:
            try:
                if self.Exists(path)==False:
                    os.mkdir(path)
                break
            except WindowsError:
                self.MakePath( os.path.join(path, "..") )

    def GetSize(self, path):
        """ Recursively adds all returned values of individual file size """
        if os.path.isdir(path):
            total = 0
            for root, dirs, files in os.walk(path):
                for f in files:
                    total += os.path.getsize( os.path.join(root, f))
            return total
        else: return os.path.getsize(path)

    def GetDetails(self):
        """ Used to print extensive details from the "Extended Menu" """
        cwd = os.getcwd()
        sVer = sys.version

        items = [_Fancy, 
                "\nScript Location: %s \nCache Location: %s \nArchive Location: %s " % (_ScriptLoc, _CacheLoc, _UsersLoc),
                 "Current Directory: %s \n\nProgram Version: %s \nSystem Version %s " % (cwd, __version__, sVer),
                 "\nRelease Date: %s \nCopyright: %s \nAuthor: %s \n" % (__date__, __copyright__, __author__)
                 ]
        for line in items: print line
                 
    def Clean(self, Path, verbose=True):
        """ Utilizes various methods to remove data from Path """
        try:
            if os.path.isdir(Path):
                shutil.rmtree(Path)
            else:
                if os.path.isfile(Path):
                    self.WriteFile(Path, self.RandomString(2**8, True) )
                os.remove(Path)
        except Exception as E:
            if verbose: print '\nUnable to remove file(s)!\nPlease close any open processes!\n', E
            return False
            
    def Log(self, Stat, LogName= _LogLoc ):
        """ Obsolete method to log events. \nMay go away """
        self.WriteFile(LogName, '\n\n'+Stat, 'a')
                
    def ReadFile(self, FileName, mode='rb'):
        """ Reads and returns all contents of file """
        with file(FileName, mode) as f:
            return f.read()
            
    def WriteFile(self, FileName, Content, mode='wb'):
        """ Forecfully writes specified content to file. Use with caution! """
        with file(FileName, mode) as f:
            f.write(Content)
        f.close()
        
    def RandomString(self, length=10, CanExist=False ):
        """ Generates random string """
        minim = length/60
        size = random.randint(4+mod, 8+mod)
        BaseChars = (string.ascii_letters + string.digits) * size
        while True:
            Out = ''.join( random.sample( BaseChars, min(length, size) ) )
            if self.Exists(Out) == CanExist:
                return Out
                
    def Smart_Input(self, msg='(Y/N)'):
        """ Extended raw_input with system functions"""
        while True:
            Out = raw_input(msg)
            OutUp = Out.upper()
            LOO = len(Out)
            path = Out[2:].strip(' ') ## Used for "CD"
            if path.upper() in ["HOME"]: path = _ScriptLoc
            if OutUp in self.ExitCode and len(Out)==4:
                raise SystemExit
            elif OutUp in ["LS", "DIR"]:
                print _Fancy, os.listdir('.')
            elif OutUp in ["GWD", "PWD"]:
                print _Fancy, os.getcwd()
            elif OutUp in ["FAQ", "HELP"]:
                print _Fancy, FAQ
            elif OutUp in "GETINFO":
                self.GetDetails()
            elif OutUp in ["START", "OPEN"]:
                os.startfile('.')
            elif OutUp == "LOGOUT":
                raise EnvironmentError
            elif OutUp[:2]=="CD" and self.Exists(path):
                os.chdir(path)
                print "\nChanging directories to: \n%s \n" % os.getcwd()
            else:
                return Out
            
    def Raw_Choice(self, Msg='(Y/N)', Options='YN', Length=1):
        """ User input specific answer choice """
        while True:
            Answer = self.Smart_Input(Msg+'> ').upper()
            if Answer in Options and len(Answer)==Length:
                return Answer
                
    def MakeASCII(self, String):
        """ Filters out invalid characters """
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
        """ Gets login credentials form user input """
        while True:
            print _Fancy
            UN = self.Smart_Input('Enter User Name >>> ').upper()
            PW = self.Smart_Input('Enter Password >>> ')
            if Confirm:
                PW2 = self.Smart_Input('Confirm Password >>> ')
                if PW == PW2:
                    if UN == PW.upper():
                        print "\nUsername and password can't be the same!"
                    else:
                        Confirm=False
                else:
                    print '\nPasswords do not match!'
            if Confirm==0:
                return UN, PW
            else:
                raise EnvironmentError
                
    def GetFileName(self, UN, PW):
        """ Mix variables and Collatz algorithm to produce one-way string file name """
        DefaultPhrase = self.Vigenere('_CoMpLeXiTy_314', UN)
        P1 = self.Vigenere(DefaultPhrase, UN, True)
        P2 = self.Vigenere(P1, PW, True)
        Name = ''
        for char in P1+P2:
            cInt = self.Collatz( ord(char) * 4 )%256
            Name += chr( cInt ) if cInt>0 else ''
        return Name #(Name, P1, P2)
        
    def Collatz(self, n):
        """ Simple algorithm representation of Collatz Conjecture """
    ## Basic algorithm
        n = abs(n); numb=[]
        if n<=2: return n
        while n!=1:
            numb.append(n)
            if n%2==0 and n!=0: n/=2
            else: n=(n*3)+1
        return max(numb)

    def Vigenere(self, string, key, encrypt=None):
        """ Primary method for just single poly-alphabetic encryption """
        #return string
        LP = len(key)
        out = ''; x=0
        los = len(string)
        if "" in (string, key): return string
        for x in range( los ):
            val1, val2 = ord( string[x] ), ord( key[x % LP ] )
            if encrypt != None:
                val3 = val1+val2 if encrypt==False else val1-val2 ## if True else (False)      
            else:   
                a, b = min([val1, val2]), max([val1, val2])
                val3 = val1+val2 if (val2<val1 and val1+val2<256) else b-a
            v3 = val3%256
            out += chr(v3)
        return out
                        
    def VigLarge(self, string, key, encrypt=None, Blocks=512):
        """ Encrypts string in small blocks """
        if False: #len(string) < Blocks/2.5:
            print "\nLarge going to straight..."
            return self.Vigenere(string, key, encrypt)
        middle = len(string)/2
        a,b = middle-Blocks, middle+Blocks
        modified = string[:Blocks] + string[-Blocks:]
        viged = self.Vigenere(modified, key, encrypt)
        out = viged[:Blocks] + string[Blocks:-Blocks] + viged[-Blocks:]
        #print middle, a,b
        return out

    def MakeBlocks(self, String, Size):
        """ Creates blocks for larger string encryption """
        ## Creates blocks from string based on "Size"
        x=0; LOS=len(String)
        while x*Size < LOS: #for x in range(1, (len(String) / Size) ) :
            x += 1
            a, b = ((x-1)*Size), (x*Size)
            #print "The X: ", x, "  |\tA, B : ", a, b
            yield String[ a : b ]
                
    def VigBlocks(self, String, PW, mode=True, Size=2**15, Path=None):
        """ Used for high volumes of data. Highest block method available """
        ## Encrypts blocks for large strings
        if False: #len(String) < 2**20 :
            print "\nBlocks going to large..."
            return self.VigLarge(String, PW, mode, Size)
        LOS = len(String)
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
        """ Execute string encryption based on size of text """
        LOS = len(string)
        if LOS > 2**20:
            print "\nUsing Blocks Method..."
            product = self.VigBlocks(string, key, encrypt, 2048)
        elif LOS > 2**15:
            print "\nUsing Large Method..."
            product = self.VigLarge(string, key, encrypt, 512)
        else:
            print "\nUsing Primary Method..."
            product = self.Vigenere(string, key, encrypt)
            #product = self.Vig(string, key, encrypt, limit=2056, Blocks=512)[0]
        return product
        
Tools = SAK()


class ArcZip():
    """ Class for handling String IO and zipfile instances """
    
    def __init__(self, Active=True):
        pass
        
    def WalkDir(self, path):
        """ Generator function for directory files """
        ## Generator object for directory walks
        for root, dirs, files in os.walk(path):
            for f in files:
                yield os.path.join(root, f)
                
    def CreateZip(self, ZipName, Password):
        """ Creates zipfile containing default information """
        ## Creates archive file in local directory
        FileInst = StringIO.StringIO()
        with zipfile.ZipFile( FileInst, mode='w', compression=COMP_TYPE ) as ZipF:
            for item in DEFAULTS:
                
                if Tools.Exists(item):
                    print "\nCopying default file..."
                    ZipF.write(item, item)
                else: ZipF.writestr(item, DEFAULTS[item])
            ZipF.close()
        Encrypted = Tools.AutoVig( FileInst.getvalue(), Password, True, BLOCK)
        Tools.WriteFile(ZipName, Encrypted )
                
    def OpenZip(self, ZipName, Password):
        """ Decrypts a zipfile and returns zipfile IO instance """
        ## Opens and decrypts zip file and returns decrypted zip file instance
        raw_zip = Tools.ReadFile(ZipName)
        Decrypted = Tools.AutoVig(raw_zip, Password, False, BLOCK)
        buff = StringIO.StringIO(Decrypted)
        if zipfile.is_zipfile( buff ):
            print "\nProcessing Archive IO Instance..."
            ZipInst = zipfile.ZipFile( buff, 'r', compression=COMP_TYPE )
            return ZipInst
        else: return False  
        
    def WriteZip(self, TmpDir, Password=None, Destination=None):
        """ Reads all files in temp directory in writes to zipfile """
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
        """ Extracts all files in a decrypted zipfile instance """
        #Extracts all files in decrypted Zip IO instance
        if ToDir==None: ToDir = self.ToDir
        if Tools.Exists(ToDir)==0: Tools.MakePath(ToDir)
        ZipInst.extractall( ToDir )
        
class User(ArcZip):
    """ Primary UI class for Zip Archive Usage """
    
    def __init__(self, Active=True):
        self.Username, self.Password = '', ''
        self.ZipName, self.ZipInst = '', None
        self.ToDir, self.ZipBackup = '', ''
            
        if Active:
            os.chdir(_ScriptLoc)
            Tools.CD(_ScriptLoc)
            if Tools.Exists(_CacheLoc):
                Tools.Clean (_CacheLoc, False)
            if Tools.Exists(_CacheLoc)==False:
                os.mkdir(_CacheLoc)
            if Tools.Exists(_UsersLoc)==False:
                os.mkdir(_UsersLoc)
            Tools.WriteFile("FAQ.txt", FAQ, 'w')
            
            self.Start()
    
    def Depart(self, Cleanup=True, verbose=True):
        """ Method to safely exit program, removing cache files """
        print _Fancy, '\nGoodBye!' if verbose else ""
        Tools.Clean(_CacheLoc)
        time.sleep(3)
        sys.exit()
        ## Delete Tmp Dir...
    
    def UpdateUserVar(self, Switch):
        """ Gathers primary user variables, stores globally within class """
        self.Username, self.Password = Tools.GetLogin( Switch ) #'CHRIS', 'ares'
        Name = Tools.MakeASCII(Tools.GetFileName(self.Username, self.Password) )[:20]+'.ADF'
        self.ZipName = os.path.join( _ScriptLoc, "_Users", Name)
        self.ZipBackup = os.path.join( _ScriptLoc, "_Users", Name.replace(".ADF", ".ABDF"))
        RawDir = Name.rstrip('.ADF')
        self.ToDir = os.path.join(_ScriptLoc, '_Cache', ".$"+RawDir) ##'.$'
            
    def Start(self):
        """ First menu interface to start archive process """
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
                ArcStatBak = Tools.Exists(self.ZipBackup)
                if Either==False:
                    if ArcStat or ArcStatBak:
                        if ArcStat:
                            shutil.copy(self.ZipName, self.ZipBackup)
                            self.ZipInst = self.OpenZip(self.ZipName, self.Password )
                        else:
                            print "\nRestoring from backup file..."
                            shutil.copy(self.ZipBackup, self.ZipName)
                            self.ZipInst = self.OpenZip(self.ZipBackup, self.Password )
                        if self.ZipInst != False: self.Run()
                        else: print "\nUnable to proccess archive!" 
                     
                    else:
                        print "\nAccount not found!"
                else:
                    if ArcStat==0:
                        self.CreateZip(self.ZipName, self.Password)
                        print "\nAccount created successfully! \nPlease re-login to continue!"
                    else: 
                        print "\nArchive already exists. Please log in instead."
                
    def Run(self):
        """ UI for Archive instances once variables are established """
        Menu1 = "MAIN MENU: \na. Start Archive \tb. Save Archive \nc. More \t\td. Logout"
        Menu2 = "EXTENDED MENU: \na. Clear Cache \t\tb. Delete Archive \nc. Info \t\td. Back"
        Msg, Options = "(A/B/C/D)", "ABCD"
        MainMenu = True
        print _Fancy, "\nWelcome %s!" % self.Username.title() 
        while True:
            Tools.Sleep(2)
            print _Fancy, Menu1 if MainMenu else Menu2
            Choice = Tools.Raw_Choice(Msg, Options)
            if MainMenu == True:
                if Choice=="C": MainMenu=False
                else: self.MainMenu(Choice)
            else:
                if Choice=="D": MainMenu=True
                self.ExtendedMenu(Choice)

    def ExtendedMenu(self, Choice):
        """ Extended menu for alternitive options """
        if Choice == "A":
            if Tools.Exists(self.ToDir):
                print "\nWarning: Any unsaved changes to your archive will be lost!"
                c = Tools.Raw_Choice("Continue? (Y/N) > ")
                if c=="N": return
                else: print "\nProceeding..."
            if Tools.Exists(_CacheLoc):
                for x in range(100):
                    Tools.Clean( _CacheLoc, False )
                    if Tools.Exists(_CacheLoc)==0:
                        print "\nCache has been cleared!"
                        break
                    time.sleep(.1)
            else: print "\nLocal Cache already cleared!"
        elif Choice == "B":
            self.RemoveArchive()
        elif Choice=="C":
            Tools.GetDetails()

    def MainMenu(self, Choice):
        """ Main menu with basic archive control """
        if Choice == 'A':
            self.StartArchive()
        elif Choice == 'B':
            self.SaveArchive()
        elif Choice=="D":
            self.LogOut()

    def LogOut(self):
        """ Logout current user and returns to Master Menu """
        if Tools.Exists(self.ToDir):
            print "\nWarning! Did you want to save your archive first?"
            Ans = Tools.Raw_Choice()
            if Ans == "Y": self.SaveArchive()
        raise EnvironmentError

    def RemoveArchive(self):
        """ Removes Archive and temp directory if one exists. May use "SUOVW" in place of captcha """
        print "\nConfirm removale of entire archive \nby entering the Captcha between > and <:"
        code = Tools.RandomString(6, False)
        attempt = raw_input("@#!>%s<?*@ \n> " % code)
        OVW = "SUOVW" ; CONT=False
        if attempt==code or attempt==OVW:
            if attempt != OVW:
                print "\nNow re-login: "
                a, b = Tools.GetLogin(False)
                if (a,b) == (self.Username, self.Password):
                    CONT = True
                else: print "\nIncorrect login!"
            else: CONT=True
            if CONT==True:
                stat = Tools.Clean(self.ZipName)
                stat = Tools.Clean(self.ZipBackup)
                if stat != False:
                    print "\nArchive has been removed!"
                    raise EnvironmentError
                else:
                    print "\nUnable to remove archive at this time!"
            
        else: print "\nIncorrect Captcha!"


    def StartArchive(self):
        """ Opens zipfile and decrompresses content into temp directory """
        if Tools.Exists(self.ToDir):
            print "\nAn archive is already started. Please Save or manually remove direcory: \n%s " % self.ToDir
        else:
            os.mkdir(self.ToDir)
            self.Decompress(self.ZipInst, self.ToDir)
            print "\nArchive has been opened at: \n%s " % (self.ToDir)
            
            try: os.startfile(self.ToDir)
            except: pass
    def SaveArchive(self):
        """ Reads, encrypts, and writes files back into zipfile container """
        if Tools.Exists(self.ToDir): # and Update==False:
            a, b = Tools.GetSize(self.ToDir), Tools.GetSize(self.ZipName)
            if a < b and b>1:
                print "\nDetected changes are less than original archive file size!"
                if a<1:
                    print "\nAll file(s) will be removed!\n"
                if Tools.Raw_Choice("Proceed with changes? (Y/N) >")=="N": return
            print '\nSaving...'
            ZipInstByte = self.WriteZip(self.ToDir, self.Password, self.ZipName )
            RmStat = Tools.Clean( self.ToDir )
            print "\nArchive has been saved!"
            print "...and the temporary directory %s removed" % ("WAS" if RmStat!=False else "WAS NOT") 
            print "Location: ", os.path.relpath( self.ToDir )
            self.ZipInst = self.OpenZip(self.ZipName, self.Password) ## Update
            shutil.copy(self.ZipName, self.ZipBackup)
            
        else:
            print "\nArchive not started! \nNo changes made to archive!"


if __name__=="__main__":
    if "win" in sys.platform:
        os.system("cls & color a & title Archive V.%s" % __version__ )
    while True:
        try:
            UserInst = User()
        except EnvironmentError:
            ## Reesults in returning to primary login screen "Master Menu"
            pass
        except SystemExit:
            if Tools.Exists(_CacheLoc):
                print "\nClearing...\n"
                Tools.Clean(_CacheLoc)
            print "\nExiting...\n"
            break
