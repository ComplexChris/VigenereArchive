# coding: utf-8


## Container Archive Encryption Program
## Written and Devoloped by Chris J. Nguyen
# rgetroiherihsiyurg


import os, sys, zipfile, StringIO, string, random, shutil, time

__version__ = "2.2.7"
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
    
    def Clean(self, Directory, verbose=True):
        try:
            shutil.rmtree(Directory)
        except Exception as E:
            if verbose: print '\nUnable to remove directory!\nPlease close any open processes!\n', E
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

    def VigWrite(self, strings, key, encrypt=None, limit=2056, Path=None, Block=512):
        ## Encrypts large blocks and writes to file
        ## Saves memory for higher encryption calls
        with file(Path, 'w') as f:
            pass
        
    def Vig(self, strings, key, encrypt=None, limit=2056, Blocks=512):
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

            #print "\nLength = ", len(string)
            #print string
            if len(string)>limit:
                print "\nApplying Smart Engine..\n"
                
                ORG = string
                middle = len(string)/2
                a,b = middle-Blocks, middle+Blocks
                modified = string[:Blocks] + string[-Blocks:]
                out = self.Vig(modified, key, encrypt, limit) [0]
                out = out[:Blocks] + string[Blocks:-Blocks] + out[-Blocks:]
            else:
                out = ''; x=0
                los = len(string)
                block = len( str(los) ) - (1 if los>10 else 0 )
                for x in range( los ):
                    if x%block == 0:
                        val1, val2 = ord( string[x] ), ord( key[x % LP ] )
                        if encrypt != None:
                            val3 = val1+val2 if encrypt else val1-val2 ## if True else (False)      
                        else:   
                            a, b = min([val1, val2]), max([val1, val2])
                            val3 = val1+val2 if (val2<val1 and val1+val2<256) else b-a
                        v3 = val3%256
                        out += chr(v3) # if v3>0 else ''
                        
                    else:
                        out+=string[x]
            products.append( out )      
        return products

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
                val3 = val1+val2 if encrypt else val1-val2 ## if True else (False)      
            else:   
                a, b = min([val1, val2]), max([val1, val2])
                val3 = val1+val2 if (val2<val1 and val1+val2<256) else b-a
            v3 = val3%256
            out += chr(v3)
        return out
                        
    def VigLarge(self, string, key, encrypt=None, Blocks=512):
        if len(string) < Blocks/2.5:
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
                
    def VigBlocks(self, String, PW, mode=True, Size=1024, Path=None):
        ## Encrypts blocks for large strings
        if len(String) < Size/4 :
            print "\nBlocks going to large..."
            return self.VigLarge(String, PW, mode, Size/4)
        LOS = len(String)
        #Tools.WriteFile(Path, '')
        x=-1
        mass = ''
        for part in self.MakeBlocks(String, Size):
            x+=1
            #frag = String[ (x-1)*BlockSize : x*BlockSize ]
            if x % 2 == 0:
                chunk = Tools.VigLarge(part, PW, mode, Size/4) # Tools.VigLarge( part, PW, mode, cap )
            else:
                chunk = part
            mass += chunk
            #Tools.WriteFile(Path, chunk, "ab")
        return mass

    def AutoVig(self, string, key, encrypt=None, Blocks=512):
        LOS = len(string)
        if LOS > 4096:
            print "Using Blocks"
            product = self.VigBlocks(string, key, encrypt, Blocks=512)
        elif LOS > 2048:
            print "Using Large"
            product = self.VigLarge(string, key, encrypt, Blocks=512)
        else:
            print "Using Reg"
            product = self.Vigenere(string, key, encrypt)
            #product = self.Vig(string, key, encrypt, limit=2056, Blocks=512)[0]
        return product

    def Bench(self, size = 128):
        raw = Tools.ReadFile("Zip.py")
        a = Tools.VigBlocks(raw, "ares", True, size, "TestSmall.txt")
        #raw2 = Tools.ReadFile("TestSmall.txt")
        b = Tools.VigBlocks(a, "ares", False, size)
        print raw==b
        return a, b
        
    def BenchAud(self, size = 128):
        raw = Tools.ReadFile("Ellie Goulding - Figure 8 (Xilent Remix) - aBwdpzIBBaw.m4a")
        Tools.VigBlocks("TestAud.m4a", "ares", raw, True, size, 8)
        raw2 = Tools.ReadFile("TestAud.m4a")
        Tools.VigBlocks("TestAudDEC.m4a", "ares", raw2, False, size, 8)
        
    def Bench2(self):
        print "Encrypting"
        raw = Tools.ReadFile("Zip.py")
        a = Tools.VigLarge( raw, 'ares', True, 32)
        Tools.WriteFile("TestEnc.py", a)
        b = Tools.VigLarge(a, "ares", False, 32)
        Tools.WriteFile("TestDec.py", b)
        
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
        with zipfile.ZipFile( FileInst, mode='w', compression=COMP_TYPE ) as ZipF:
            #for raw_file in WalkDir( TmpDir ):
            ZipF.writestr('MyPasswords.txt', 'Facebook = "Bob1992" ')
            ZipF.writestr('MyNotes.txt', 'To do: Decrypt Russian Nuclear Launch Codes "XMG-01 (WMD)" ')
            ZipF.close()
        #print FileInst.getvalue()
        #Tools.WriteFile("DecArc.zip", FileInst.getvalue())
        Encrypted = Tools.VigBlocks( FileInst.getvalue(), Password, True, BLOCK)
        print "\nNew Encrypted: ", Encrypted
        Tools.WriteFile(ZipName, Encrypted )
                
    def OpenZip(self, ZipName, Password):
        global buff, ZipInst
        ## Opens and decrypts zip file and returns decrypted zip file instance
        raw_zip = Tools.ReadFile(ZipName)
        Decrypted = Tools.VigBlocks(raw_zip, Password, False, BLOCK)
        print Decrypted
        buff = StringIO.StringIO(Decrypted)
        Tools.WriteFile("DecArc.zip", Decrypted)
        if zipfile.is_zipfile( buff ):
            print "\nOpening Archive..."
            print "\nOpened Decrypted: ", Decrypted
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
            #print "\nValue = " , FileInst.getvalue()
            Path = os.path.join(_ScriptLoc, Destination), Encrypt
            Encrypt = Tools.VigBlocks(FileInst.getvalue(), Password, True, BLOCK)
            Tools.WriteFile(Path, Encrypt)
            #print "\nEncrypted = " , Encrypt

    def Decompress(self, ZipInst, ToDir = None ):
        print ZipInst.filelist
        Tools.Log (str("Decompressing: "+ToDir))
        if ToDir==None: ToDir = self.ToDir
        ZipInst.extractall( ToDir )
        
class User(ArcZip):
    
    def __init__(self, Active=True):
        if Active:
            Tools.CD(_ScriptLoc)
            if Tools.Exists(_CacheLoc):
                Tools.Clean (_CacheLoc)
            if Tools.Exists(_CacheLoc)==False: os.mkdir(_CacheLoc)

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
                    if True: #ArcStat==0:
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
            print _Fancy, Menu1
            Choice = Tools.Raw_Choice(Msg, Options)
            
            if Choice == 'A':
                if Update:
                    Update=False
                    Tools.CD(_ScriptLoc)
                    self.ZipInst = self.OpenZip(self.ZipName, self.Password)

                if Tools.Exists(self.ToDir):
                    print "\nAn archive is already started. Please Save or manually remove direcory: \n%s " % self.ToDir
                    continue
                else:
                    self.Decompress(self.ZipInst, self.ToDir)
                    print "\nArchive has been opened at: \n%s " % (self.ToDir)
                    
                    try: os.startfile(self.ToDir)
                    except: continue
                
            elif Choice == 'B':
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
            elif Choice=='C':
                print "\nComing soon..."
            else:
                self.__init__()
                return
                
if __name__=="__main__":
    pass #c = User()
