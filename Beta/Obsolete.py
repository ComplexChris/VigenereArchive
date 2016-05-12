

class Obsolete():

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
