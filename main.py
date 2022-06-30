import math as m
from PyQt5 import QtCore
import os

global text

class tredent(QtCore.QThread):
    
    def __init__(self, parent, func):
        
        super(tredent, self).__init__(parent)
        self.kjamba = lambda:func()
        # self.func = func
        
    def run(self):
        self.kjamba()
        
        # self.func()


class Logic(QtCore.QThread):
    
    uppb = QtCore.pyqtSignal(int)
    sigl = QtCore.pyqtSignal(str)
   
    
    def __init__(self, parent, abasid, key_txt, tip, vopros) :
        super(Logic, self).__init__(parent)
        self.abasid = abasid
        self.key_txt =key_txt
        self.tip = tip
        self.vopros = vopros
        self.mas_ef = {"ECB": lambda a, b,c: self.ECB(a,b,c), "CBC": lambda a, b,c: self.CBC(a,b,c), "CFB": lambda a, b,c: self.CFB(a,b,c), "OFB": lambda a, b,c: self.OFB(a,b,c)}
        self.mas_def = {"ECB": lambda a, b,c: self.D_ECB(a,b,c), "CBC": lambda a, b,c: self.D_CBC(a,b,c), "CFB": lambda a, b,c: self.D_CFB(a,b,c), "OFB": lambda a, b,c: self.D_OFB(a,b,c)}
        self.endec = [1, 45, 226, 147, 190, 69, 21, 174,
                    120, 3, 135, 164, 184, 56, 207, 63, 8, 103, 9, 148, 235, 38, 168, 107,
                    189, 24, 52, 27, 187, 191, 114, 247, 64, 53, 72, 156, 81, 47, 59, 85,
                    227, 192, 159, 216, 211, 243, 141, 177,
                    255, 167, 62, 220, 134, 119, 215, 166, 17, 251, 244, 186, 146, 145, 100, 131,
                    241, 51, 239, 218, 44, 181, 178, 43,
                    136, 209, 153, 203, 140, 132, 29, 20,
                    129, 151, 113, 202, 95, 163, 139, 87, 60, 130, 196, 82, 92, 28, 232, 160, 4, 180, 133, 74, 246, 19, 84, 182,
                    223, 12, 26, 142, 222, 224, 57, 252, 32, 155, 36, 78, 169, 152, 158, 171,
                    242, 96, 208, 108, 234, 250, 199, 217, 0, 212, 31, 110, 67, 188, 236, 83,
                    137, 254, 122, 93, 73, 201, 50, 194,
                    249, 154, 248, 109, 22, 219, 89, 150, 68, 233, 205, 230, 70, 66, 143, 10,
                    193, 204, 185, 101, 176, 210, 198, 172, 30, 65, 98, 41, 46, 14, 116, 80, 2, 90, 195, 37, 123, 138, 42, 91,
                    240, 6, 13, 71, 111, 112, 157, 126, 16, 206, 18, 39, 213, 76, 79, 214,
                    121, 48, 104, 54, 117, 125, 228, 237,
                    128, 106, 144, 55, 162, 94, 118, 170,
                    197, 127, 61, 175, 165, 229, 25, 97,
                    253, 77, 124, 183, 11, 238, 173, 75, 34, 245, 231, 115, 35, 33, 200, 5,
                    225, 102, 221, 179, 88, 105, 99, 86, 15, 161, 49, 149, 23, 7, 58, 40]

        self.antiendec = [128, 0, 176, 9, 96, 239, 185, 253, 16, 18, 159, 228, 105, 186, 173, 248,
                        192, 56, 194, 101, 79, 6, 148, 252, 25, 222, 106, 27, 93, 78, 168, 130,
                        112, 237, 232, 236, 114, 179, 21, 195,
                        255, 171, 182, 71, 68, 1, 172, 37,
                        201, 250, 142, 65, 26, 33, 203, 211, 13, 110, 254, 38, 88, 218, 50, 15, 32, 169, 157, 132, 152, 5, 156, 
                        187, 34, 140, 99, 231, 197, 225, 115, 198,
                        175, 36, 91, 135, 102, 39, 247, 87,
                        244, 150, 177, 183, 92, 139, 213, 84,
                        121, 223, 170, 246, 62, 163, 241, 17,
                        202, 245, 209, 23, 123, 147, 131, 188,
                        189, 82, 30, 235, 174, 204, 214, 53, 8, 200, 138, 180, 226, 205, 191, 217,
                        208, 80, 89, 63, 77, 98, 52, 10, 72, 136, 181, 86, 76, 46, 107, 158,
                        210, 61, 60, 3, 19, 251, 151, 81,
                        117, 74, 145, 113, 35, 190, 118, 42, 95, 249, 212, 85, 11, 220, 55, 49, 22, 116, 215, 119, 167, 230, 7, 219,
                        164, 47, 70, 243, 97, 69, 103, 227, 12, 162, 59, 28, 133, 24, 4, 29, 41, 160, 143, 178, 90, 216, 166, 126,
                        238, 141, 83, 75, 161, 154, 193, 14,
                        122, 73, 165, 44, 129, 196, 199, 54, 43, 127, 67, 149, 51, 242, 108, 104,
                        109, 240, 2, 40, 206, 221, 155, 234, 94, 153, 124, 20, 134, 207, 229, 66,
                        184, 64, 120, 45, 58, 233, 100, 31,
                        146, 144, 125, 57, 111, 224, 137, 48]

    def run(self):
        # self.txt_f = self.openFile_C(self.abasid)
        self.lst_key = self.gen_key(self.key_txt)
        
       
        if self.vopros:
            self.shifr_tr(self.abasid, self.lst_key, self.tip) 
        else:
            self.deshifr_tr(self.abasid, self.lst_key, self.tip)
        

    # def saveFile_C(self, file):
    #     bibika = text.to_bytes((text.bit_length()+7)//8, byteorder="big")
    #     with open(file, "wb") as rest:
    #         rest.write(bibika)



    # def openFile_C(self, file):
    #     with open(file, "rb") as handle:
    #         faile = bytes(handle.read())
    #         inta = int.from_bytes(faile, byteorder='big')
    #         return inta

    def delitel(self, inta):
        gulag =  int(m.ceil(inta.bit_length() / 64 ))
        
        s = []
        for i in range (0, gulag):
            s.append(inta&((1<<64)-1))
            inta =inta>>64
          
        return s

            
    def gen_key(self, key):
        key_lst = []
        key = key.encode('ascii')   
        key = int.from_bytes(key, byteorder='big')  
        
        for i in range(2,14):
            key_lst_t =[]
            for j in range (1, 9):
                a = ((key<<3*i)+(45**((9*i+j)%256)%257)%257)%256
                key_lst_t.append(a)
            key_lst.append(key_lst_t[0])
            for k in range (2, 9):
                key_lst[i-2]=(key_lst[i-2]<<8)|key_lst_t[k-2]
        key_lst.insert(0, key)
        print(key_lst)
        return key_lst 



        

    def shifrovanie(self, bit_sh, key_lst):
        for j in range (0, 6):
            round_key1 = key_lst[2*j] 
            round_key2 =key_lst[2*j+1] 
            bit_sh_k1 = []
            bit_sh_k2 = []
            for k in range (0, 8):
                bit_sh_k1.append(round_key1&((1<<8)-1))
                round_key1 =round_key1>>8
            for k in range (0, 8):
                bit_sh_k2.append(round_key2&((1<<8)-1))
                round_key2 =round_key2>>8
           
            # первое действие 
            bit_sh[0] =bit_sh[0]^bit_sh_k1[0]
            bit_sh[3] =bit_sh[3]^bit_sh_k1[3]
            bit_sh[4] =bit_sh[4]^bit_sh_k1[4]
            bit_sh[7] =bit_sh[7]^bit_sh_k1[7]
            bit_sh[1] =(bit_sh[1]+bit_sh_k1[1])%256
            bit_sh[2] =(bit_sh[2]+bit_sh_k1[2])%256
            bit_sh[5] =(bit_sh[5]+bit_sh_k1[5])%256
            bit_sh[6] =(bit_sh[6]+bit_sh_k1[6])%256
            

            #второе действие 
            bit_sh[0] = self.endec[bit_sh[0]]
            bit_sh[3] = self.endec[bit_sh[3]]
            bit_sh[4] = self.endec[bit_sh[4]]
            bit_sh[7] = self.endec[bit_sh[7]]
            bit_sh[1] = self.antiendec[bit_sh[1]]
            bit_sh[2] = self.antiendec[bit_sh[2]]
            bit_sh[5] = self.antiendec[bit_sh[5]]
            bit_sh[6] = self.antiendec[bit_sh[6]]

            #третье действие 
            bit_sh[0] =(bit_sh[0]+bit_sh_k2[0])%256
            bit_sh[3] =(bit_sh[3]+bit_sh_k2[3])%256
            bit_sh[4] =(bit_sh[4]+bit_sh_k2[4])%256
            bit_sh[7] =(bit_sh[7]+bit_sh_k2[7])%256
            bit_sh[1] =bit_sh[1]^bit_sh_k2[1]
            bit_sh[2] =bit_sh[2]^bit_sh_k2[2]
            bit_sh[5] =bit_sh[5]^bit_sh_k2[5]
            bit_sh[6] =bit_sh[6]^bit_sh_k2[6]

            #четвертое действие - псевдопреобразование Адамара
            bit_ksh = [0,0,0,0,0,0,0,0,]
            bit_ksh[0] =(2*bit_sh[0]+bit_sh[1])%256
            bit_ksh[1] =(bit_sh[0]+bit_sh[1])%256
            bit_ksh[2] =(2*bit_sh[2]+bit_sh[3])%256
            bit_ksh[3] =(bit_sh[2]+bit_sh[3])%256
            bit_ksh[4] =(2*bit_sh[4]+bit_sh[5])%256
            bit_ksh[5] =(bit_sh[4]+bit_sh[5])%256
            bit_ksh[6] =(2*bit_sh[6]+bit_sh[7])%256
            bit_ksh[7] =(bit_sh[6]+bit_sh[7])%256

            bit_sh[0] =bit_ksh[0]
            bit_sh[3] =bit_ksh[3]
            bit_sh[4] =bit_ksh[4]
            bit_sh[7] =bit_ksh[7]
            bit_sh[1] =bit_ksh[1]
            bit_sh[2] =bit_ksh[2]
            bit_sh[5] =bit_ksh[5]
            bit_sh[6] =bit_ksh[6]

        #ластетский раунд с одним ключем - апендикосм 
        round_key1 = key_lst[12] 
        bit_sh_k1=[]
        for k in range (0, 8):
                bit_sh_k1.append(round_key1&((1<<8)-1))
                round_key1 =round_key1>>8
        bit_sh[0] =bit_sh[0]^bit_sh_k1[0]
        bit_sh[3] =bit_sh[3]^bit_sh_k1[3]
        bit_sh[4] =bit_sh[4]^bit_sh_k1[4]
        bit_sh[7] =bit_sh[7]^bit_sh_k1[7]
        bit_sh[1] =(bit_sh[1]+bit_sh_k1[1])%256
        bit_sh[2] =(bit_sh[2]+bit_sh_k1[2])%256
        bit_sh[5] =(bit_sh[5]+bit_sh_k1[5])%256
        bit_sh[6] =(bit_sh[6]+bit_sh_k1[6])%256     
        return bit_sh


    def deshifrovanie(self, bit_sh, key_lst): 
        bit_sh_k1 = []  
        round_key1 = key_lst[12] 
        for k in range (0, 8):
            bit_sh_k1.append(round_key1&((1<<8)-1))
            round_key1 =round_key1>>8
                            
        bit_sh[0] =bit_sh[0] ^ bit_sh_k1[0]
        bit_sh[3] =bit_sh[3]^bit_sh_k1[3]
        bit_sh[4] =bit_sh[4]^bit_sh_k1[4]
        bit_sh[7] =bit_sh[7]^bit_sh_k1[7]
        bit_sh[1] =(bit_sh[1]-bit_sh_k1[1])%256
        bit_sh[2] =(bit_sh[2]-bit_sh_k1[2])%256
        bit_sh[5] =(bit_sh[5]-bit_sh_k1[5])%256
        bit_sh[6] =(bit_sh[6]-bit_sh_k1[6])%256
        for j in range (0, 6):
            round_key2 = key_lst[11-2*j] 
            round_key1 =key_lst[10-2*j] 
            bit_sh_k1 = []
            bit_sh_k2 = []            
            for k in range (0, 8):
                bit_sh_k1.append(round_key1&((1<<8)-1))
                round_key1 =round_key1>>8
            for k in range (0, 8):
                bit_sh_k2.append(round_key2&((1<<8)-1))
                round_key2 =round_key2>>8
            bit_ksh = [0,0,0,0,0,0,0,0]

            bit_ksh[0] =(bit_sh[0]-bit_sh[1])%256
            bit_ksh[1] =(-bit_sh[0]+2*bit_sh[1])%256
            bit_ksh[2] =(bit_sh[2]-bit_sh[3])%256
            bit_ksh[3] =(-bit_sh[2]+2*bit_sh[3])%256
            bit_ksh[4] =(bit_sh[4]-bit_sh[5])%256
            bit_ksh[5] =(-bit_sh[4]+2*bit_sh[5])%256
            bit_ksh[6] =(bit_sh[6]-bit_sh[7])%256
            bit_ksh[7] =(-bit_sh[6]+2*bit_sh[7])%256
            
            bit_sh[0] =bit_ksh[0]
            bit_sh[3] =bit_ksh[3]
            bit_sh[4] =bit_ksh[4]
            bit_sh[7] =bit_ksh[7]
            bit_sh[1] =bit_ksh[1]
            bit_sh[2] =bit_ksh[2]
            bit_sh[5] =bit_ksh[5]
            bit_sh[6] =bit_ksh[6]

            bit_sh[0] =(bit_sh[0]-bit_sh_k2[0])%256
            bit_sh[3] =(bit_sh[3]-bit_sh_k2[3])%256
            bit_sh[4] =(bit_sh[4]-bit_sh_k2[4])%256
            bit_sh[7] =(bit_sh[7]-bit_sh_k2[7])%256
            bit_sh[1] =bit_sh[1]^bit_sh_k2[1]
            bit_sh[2] =bit_sh[2]^bit_sh_k2[2]
            bit_sh[5] =bit_sh[5]^bit_sh_k2[5]
            bit_sh[6] =bit_sh[6]^bit_sh_k2[6]
            
            bit_sh[0] = self.antiendec[bit_sh[0]]
            bit_sh[3] = self.antiendec[bit_sh[3]]
            bit_sh[4] = self.antiendec[bit_sh[4]]
            bit_sh[7] = self.antiendec[bit_sh[7]]
            bit_sh[1] = self.endec[bit_sh[1]]
            bit_sh[2] = self.endec[bit_sh[2]]
            bit_sh[5] = self.endec[bit_sh[5]]
            bit_sh[6] = self.endec[bit_sh[6]]
            
            bit_sh[0] =bit_sh[0] ^ bit_sh_k1[0]
            bit_sh[3] =bit_sh[3]^bit_sh_k1[3]
            bit_sh[4] =bit_sh[4]^bit_sh_k1[4]
            bit_sh[7] =bit_sh[7]^bit_sh_k1[7]
            bit_sh[1] =(bit_sh[1]-bit_sh_k1[1])%256
            bit_sh[2] =(bit_sh[2]-bit_sh_k1[2])%256
            bit_sh[5] =(bit_sh[5]-bit_sh_k1[5])%256
            bit_sh[6] =(bit_sh[6]-bit_sh_k1[6])%256            
        return(bit_sh)
            
    def ECB(self, bit, key_lst,cbc_vector):
        text_sh = []
       
        for i in range (0, len(bit)):
          
            round_word = bit[i]
            bit_sh = []
            for k in range (0, 8):
                    bit_sh.append(round_word&((1<<8)-1))
                    round_word =round_word>>8
            bit_sh = self.shifrovanie(bit_sh, key_lst)
            text_sh.append(bit_sh[7])
            for k in range (0, 7):
                text_sh[i]=(text_sh[i]<<8)|bit_sh[6-k]
            text_sh[i] = text_sh[i]^cbc_vector
       
        end_sh = text_sh[len(text_sh)-1]
        
        for i in range (0, len(text_sh)-1):
            end_sh=(end_sh<<64)|text_sh[len(text_sh)-2-i]
       
        return(end_sh)
    def CBC(self, bit, key_lst, cbc_vector):
        text_sh = []
        
        for i in range (0, len(bit)):
            if i == 0:
                round_word = bit[i]^cbc_vector     
            else:
                round_word = bit[i]^text_sh[i-1]
            
            bit_sh = []
            for k in range (0, 8):
                    bit_sh.append(round_word&((1<<8)-1))
                    round_word =round_word>>8
            bit_sh = self.shifrovanie(bit_sh, key_lst)
            text_sh.append(bit_sh[7])
            for k in range (0, 7):
                text_sh[i]=(text_sh[i]<<8)|bit_sh[6-k]
        
        end_sh = text_sh[len(text_sh)-1]
        
        for i in range (0, len(text_sh)-1):
            end_sh=(end_sh<<64)|text_sh[len(text_sh)-2-i] 
        return(end_sh)
    
    def CFB(self, bit, key_lst, cbc_vector  ):
        text_sh = []
        
        for i in range (0, len(bit)):              
           
            if i ==0:    
                round_word = cbc_vector
            else:
                round_word = text_sh[i-1]
            
            bit_sh = []
            for k in range (0, 8):
                    bit_sh.append(round_word&((1<<8)-1))
                    round_word =round_word>>8
            
            bit_sh = self.shifrovanie(bit_sh, key_lst)
            text_sh.append(bit_sh[7])
            for k in range (0, 7):
                text_sh[i]=(text_sh[i]<<8)|bit_sh[6-k]
            
            text_sh[i]=bit[i]^text_sh[i]
           
            
                
        end_sh = text_sh[len(text_sh)-1]
        
        for i in range (0, len(text_sh)-1):
            end_sh=(end_sh<<64)|text_sh[len(text_sh)-2-i]   
         
        return(end_sh)
    
    def OFB(self, bit, key_lst, cbc_vector  ):
        text_sh = []
        
        for i in range (0, len(bit)):              
            
            if i ==0:
                round_word = cbc_vector
            
            bit_sh = []
            for k in range (0, 8):
                    bit_sh.append(round_word&((1<<8)-1))
                    round_word =round_word>>8
            
            bit_sh = self.shifrovanie(bit_sh, key_lst)
            round_word = (bit_sh[7])
            for k in range (0, 7):
                round_word=(round_word<<8)|bit_sh[6-k]
            
            text_sh.append(bit[i]^round_word)
            
                
       
        end_sh = text_sh[len(text_sh)-1]
        
        for i in range (0, len(text_sh)-1):
            end_sh=(end_sh<<64)|text_sh[len(text_sh)-2-i]
       
        return(end_sh)
    
    
    def D_ECB(self, bit, key_lst, cbc_vector  ):
        text_sh = []
        
        for i in range (0, len(bit)):
            
                
            round_word = bit[i]^cbc_vector
            bit_sh = []
            for k in range (0, 8):
                    bit_sh.append(round_word&((1<<8)-1))
                    round_word =round_word>>8
            bit_sh = self.deshifrovanie(bit_sh, key_lst)
            text_sh.append(bit_sh[7])
            for k in range (0, 7):
                text_sh[i]=(text_sh[i]<<8)|bit_sh[6-k]
            
              
        end_sh = text_sh[len(text_sh)-1]
       
        for i in range (0, len(text_sh)-1):
            end_sh=(end_sh<<64)|text_sh[len(text_sh)-2-i] 
        return(end_sh) 
    
    def D_CBC(self, bit, key_lst, cbc_vector  ):
        text_sh = []
        for i in range (0, len(bit)):            
            round_word = bit[i]
            bit_sh = []
            for k in range (0, 8):
                    bit_sh.append(round_word&((1<<8)-1))
                    round_word =round_word>>8
            
                
            bit_sh =self.deshifrovanie(bit_sh, key_lst) 
            text_sh.append(bit_sh[7])
            for k in range (0, 7):
                text_sh[i]=(text_sh[i]<<8)|bit_sh[6-k]
                
            if i == 0:
                text_sh[i] = text_sh[i]^cbc_vector
                
            else: 
                text_sh[i] = text_sh[i]^bit[i-1]
                
                
        end_sh = text_sh[len(text_sh)-1]
        for i in range (0, len(text_sh)-1):
            end_sh=(end_sh<<64)|text_sh[len(text_sh)-2-i]
        text = end_sh
        return(end_sh)
    
    def D_CFB(self, bit, key_lst, cbc_vector  ):
        text_sh = []
        
        for i in range (0, len(bit)):
            if i ==0:    
                round_word = cbc_vector
            else:
                round_word = bit[i-1]
            bit_sh = []
            
            for k in range (0, 8):
                    bit_sh.append(round_word&((1<<8)-1))
                    round_word =round_word>>8
                                
            bit_sh =self.shifrovanie(bit_sh, key_lst) 
            text_sh.append(bit_sh[7])
            for k in range (0, 7):
                text_sh[i]=(text_sh[i]<<8)|bit_sh[6-k]
                    
            
            text_sh[i]= text_sh[i]^bit[i]
           
             
        end_sh = text_sh[len(text_sh)-1]
       
        for i in range (0, len(text_sh)-1):
            end_sh=(end_sh<<64)|text_sh[len(text_sh)-2-i]
        return(end_sh)
    
    def D_OFB(self, bit, key_lst, cbc_vector  ):  
        text_sh = []  
        
        for i in range (0, len(bit)):
           
            
            
            if i ==0:
                round_word = cbc_vector
            bit_sh = []
            
            for k in range (0, 8):
                    bit_sh.append(round_word&((1<<8)-1))
                    round_word =round_word>>8
                                
            bit_sh =self.shifrovanie(bit_sh, key_lst) 
            round_word = (bit_sh[7])
            for k in range (0, 7):
                round_word=(round_word<<8)|bit_sh[6-k]
                    
            
            text_sh.append(bit[i]^round_word)
            
            
                    
        end_sh = text_sh[len(text_sh)-1]
        
        for i in range (0, len(text_sh)-1):
            end_sh=(end_sh<<64)|text_sh[len(text_sh)-2-i]
        text = end_sh
        return(end_sh)
    
    def temp_save(self, txt):
        g = txt.to_bytes(4096, byteorder="big")
        with open('temp/temp.temp', "ab") as rbk:
            rbk.write(g)
       
            
    def temp_save_l(self, txt, b):
        g = txt.to_bytes(b, byteorder="big")
        with open('temp/temp.temp', "ab") as rbk:
            rbk.write(g)
    
    def shifr_tr(self, abasid, key_lst, tip):
        self.uppb.emit(0)
        self.bambuk = 0
        key_ls = key_lst
        self.uppb.emit(0)
        cbc_vector = b"t7w!z%C*"
        cbc_vector = int.from_bytes(cbc_vector, byteorder='big')
        with open(abasid, "rb") as rest:       
            try:
                os.remove('temp/temp.temp')
                a = open("temp/temp.temp", "w+")
                a.close()
            except:
                a = open("temp/temp.temp", "w+")
                a.close()
            ac = os.path.getsize(abasid)
            
            a = int(m.ceil((ac / 4096)))
            for i in range (0, a):
                try:
                    g = int(100/(a-1)*i)
                    if g>self.bambuk  and g!=100: 
                        self.bambuk=g
                    self.uppb.emit(g)
                except:
                    pass                
                d = rest.read(4096)
                if i == a-1:
                    dived = len(d)
                b =int.from_bytes(d, byteorder='big')
                
                bit = self.delitel(b)       
                txt = self.mas_ef[tip](bit, key_ls, cbc_vector)
                self.temp_save(txt)
            
            with open('temp/temp.temp', "ab") as rbk:
                g =  dived.to_bytes(4096, byteorder="big")
                rbk.write(g)
        self.uppb.emit(100)
        string = "the process end"
        self.sigl.emit(string) 
            
                
    def deshifr_tr(self, abasid, key_lst, tip):
        self.uppb.emit(0)
        self.bambuk = 0
        key_ls = key_lst
        self.uppb.emit(0)
        cbc_vector = b"t7w!z%C*"
        cbc_vector = int.from_bytes(cbc_vector, byteorder='big')
        with open(abasid, "rb") as rest:       
            try:
                os.remove('temp/temp.temp')
                a = open("temp/temp.temp", "w+")
                a.close()
            except:
                a = open("temp/temp.temp", "w+")
                a.close()
            ac = os.path.getsize(abasid)
            
            a = int(m.ceil((ac / 4096)))
            
            for i in range (0, a-1):
                try:
                    g = int(100/(a-1)*i)
                    if g>self.bambuk  and g!=100: 
                        self.bambuk=g
                    self.uppb.emit(g)
                except:
                    pass              
                
                d = rest.read(4096)
               
                b =int.from_bytes(d, byteorder='big')
                bit = self.delitel(b)
                txt = self.mas_def[tip](bit, key_ls, cbc_vector)
                if i == a-2:
                    d = rest.read(4096)
                    b =int.from_bytes(d, byteorder='big')
                    print(b)
                    self.temp_save_l(txt, b)
                else:
                    self.temp_save(txt)
        self.uppb.emit(100)
        string = "the process end"
        self.sigl.emit(string) 
            
        
     

# bit = Logic.openFile_C('test.txt')
# # # print(bit)
# key_lst =Logic. gen_key(key)
# # # print(key_lst)
# shifr = Logic.shifrovanie(bit, key_lst)
# # # print(shifr)
# deshifr = Logic.deshifrovanie(shifr, key_lst)
# # saveFile(deshifr)