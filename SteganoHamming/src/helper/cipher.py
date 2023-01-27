import numpy as np


def Hammingcode(text): #fungsi hamming code
    G = np.array([[1,0,0,0,1,1,0],
                 [0,1,0,0,1,0,1],
                 [0,0,1,0,0,1,1],
                 [0,0,0,1,1,1,1]], dtype=np.int32) #matris generator dengan tipe int32

    a =  ''.join(format(ord(i), '08b') for i in text) #merubah string kedalam biner 8bit
    bin = np.array(list(a), dtype=np.int32) #merubah bentuk a kedalam 1 array
    bin = np.reshape (bin, (len(a)//4, 4)) #merubah bentuk array 1  baris kedalam matriks bari x, kolom 4
    c = np.matmul(bin, G) #mengalikan matriks bin dengan matriks generator
    c = c % 2 #melakukan modulo pada hasil matriks c dg tjuan merubah mnjadi 0 dan 1
    result = ''.join(''.join(str(i) for i in x) for x in c) #menggabungkan matriks kedalam char
    result = result+ '0'*(8-(len(result)%8)) #menambahkkan 0 diakhir agar berukuran kelipatan 8, untuk dilakukan bpcs
    return result

def Hammingdecode(text): #fungsi hamming decode
    H = np.array([[1,1,0,1,1,0,0],
                [1,0,1,1,0,1,0],
                [0,1,1,1,0,0,1]],dtype=np.int32) #matrik H dengan tipe int32, matriks 3x7
    synd = {'001': 6, '010':5, '100':4, '111':3, '011':2, '101':1, '110': 0} #hardcode syndrom
    a =  ''.join(format(ord(i), '08b') for i in text) #merubah string kedalam biner 8bit (ambil dari file output file txt)
    a = a[0: (len(a)- len(a)%7)] #penghapusan bit tambahan untuk diubah ke biner kelipatan 7
    bin = np.array(list(a), dtype=np.int32) #merubah bentuk a kedalam 1 array
    bin = np.reshape (bin, (len(a)//7, 7)) #merubah bentuk array 1  baris kedalam matriks bari x, kolom 7
    c = np.transpose(bin) #matriks bin di lakukan matriks transpos
    c = np.matmul(H, c) #dilakukan perkalian matriks H dengan matriks c, dengan hasil matriks [3 x X]
    c=c%2 #melakukan modulo pada hasil matriks c dg tjuan merubah mnjadi 0 dan 1
    c = np.transpose(c) #melakukan matriks transpos thrdp matriks c, hasilnya matriks [X x 3]
    err = [''.join(str(i) for i in x) for x in c] #variabel err menggabungkan matriks kedalam char

    i=0
    length=''
    temp=''
    while True: #melakukan perulangan dari i dalam range panjang variabel err
        bit = synd.get(err[i], None) #variabel bit menampung err yang sesuai dengan hardcode synd
        if bit != None: #jika bit tidak = none maka terdapat err
            wrong = np.copy(bin[i])
            bin[i][bit] = int(not(bin[i][bit])) #dilakukan perbaikan yaitu membenarkan bit yang berlawanan
            
            # print ("Terjadi kesalahan huruf ke-"+ str((i//2)+1) + ' bagian ke-'+  str(i%2+1) + 
            # ", data yang salah adalah " + ''.join(str(x) for x in wrong) +
            # " data yang benar adalah " + ''.join(str(x) for x in bin[i]) ) #str biar jdi string
        temp += ''.join(list(map(str, bin[i][0:4])))
        if len(temp)==8:
            temp=int(temp,2)
            temp=chr(temp)
            if temp=="#":
                break
            else:
                length += temp
                temp=''
        i+=1
    i+=1
    print(length)
    temp=''
    ext=''
    while True:
        bit = synd.get(err[i], None) #variabel bit menampung err yang sesuai dengan hardcode synd
        if bit != None: #jika bit tidak = none maka terdapat err
            wrong = np.copy(bin[i])
            bin[i][bit] = int(not(bin[i][bit])) #dilakukan perbaikan yaitu membenarkan bit yang berlawanan
            
            # print ("Terjadi kesalahan huruf ke-"+ str((i//2)+1) + ' bagian ke-'+  str(i%2+1) + 
            # ", data yang salah adalah " + ''.join(str(x) for x in wrong) +
            # " data yang benar adalah " + ''.join(str(x) for x in bin[i]) ) #str biar jdi string
        temp += ''.join(list(map(str, bin[i][0:4])))
        if len(temp)==8:
            temp=int(temp,2)
            temp=chr(temp)
            if temp=="#":
                break
            else:
                ext += temp
                temp=''
        i+=1
    i+=1
    print(ext)
    temp=''
    body=''
    before =''
    temp_before = ''
    while len(body) < int(length):
        temp_before += ''.join(list(map(str, bin[i][0:4])))
        bit = synd.get(err[i], None) #variabel bit menampung err yang sesuai dengan hardcode synd
        if bit != None: #jika bit tidak = none maka terdapat err
            wrong = np.copy(bin[i])
            bin[i][bit] = int(not(bin[i][bit])) #dilakukan perbaikan yaitu membenarkan bit yang berlawanan
            
            print ("Terjadi kesalahan huruf ke-"+ str((i//2)+1) + ' bagian ke-'+  str(i%2+1) + 
            ", data yang salah adalah " + ''.join(str(x) for x in wrong) +
            " data yang benar adalah " + ''.join(str(x) for x in bin[i]) ) #str biar jdi string
        temp += ''.join(list(map(str, bin[i][0:4])))
        if len(temp)==8:
            temp=int(temp,2)
            temp=chr(temp)
            body += temp
            temp=''
        i+=1

        if len(temp_before)==8:
            temp_before=int(temp_before,2)
            temp_before=chr(temp_before)
            before += temp_before
            temp_before=''
    print("string before = ",before[0:24])
    print(len(body))
    f = open("before_hamming.txt", "wb")
    f.write(before.encode("utf-8"))
    f.close()
    return length+'#'+ext+'#'+body

    # result = ''
    # temp = ''
    # for bits in bin:
    #     temp += ''.join(list(map(str, bits[0:4])))
    #     if len(temp) == 8:
    #         result += chr(int(temp, 2))
    #         temp = ''
    # return result

# if __name__ == "__main__":
#     code = list(Hammingcode("3#txt#Aku"))
#     # code[0] = str(int(not(int(code[0]))))
#     # code[14] = str(int(not(int(code[14]))))
#     bin = np.array(list(code)) #merubah bentuk a kedalam 1 array
#     bin = np.reshape (bin, (len(code)//8, 8)) #merubah bentuk array 1  baris kedalam matriks bari x, kolom 7
#     result = ''.join(chr(int(''.join(x),2)) for x in bin)
#     # result = ''.join()
#     print(Hammingdecode(''.join(result)))
#     print()