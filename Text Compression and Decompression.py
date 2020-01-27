# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 22:48:44 2019

@author: Omer Hassan
Copyrigths, all rights reserved

"""

"""
A test file is attached and the compreesed and the decompreesed version of it after running the program

the output file path is assumed to be in the same file as the code for the sake of simplicity
"""
import heapq as hq
import math
import os
import csv
def Parse(path):
    uncompressed_file=open(path,'r+')
    text_file=uncompressed_file.read()
    freq={}
    original_text=""
    for C in text_file:
        original_text+=C
        if not C in freq:
            freq[C]=1
        else:
            freq[C]+=1
    return (freq,original_text)
def prob(freq):
    pr={}
    total=0
    for k in freq:
        total+=int(freq[k])
    for k in freq:
        pr[k]=float(freq[k]/total)
    return pr
    

class Node:
    def __init__(self, val,f,level=0,b=0):
        self.val=val
        self.f=f
        self.level=level
        self.b=b#byte
        self.rightnode=None
        self.leftnode=None
    def __lt__(self, node):
        return self.f < node.f
    def __cmp__(self,node):
        return self.f>node.f
    
class Huffman_Tree:#build the tree using the imported heap
    def __init__(self):
        self.H=[]#heap
        self.encoding_dict={}
        self.decoding_dict={}
    def build_heap(self,freq):
        for val in freq:
            nd=Node(val,freq[val])
            hq.heappush(self.H, nd)
        return self.H
    def buid_tree(self):
        i=0
        while len(self.H)!=1:
            i+=1
            n1=hq.heappop(self.H)
            n2=hq.heappop(self.H)
            n12=Node(n1.val+n2.val,n1.f+n2.f,i)#merge the two nodes
            if n1>n2:#decide whther it's left or rigth to be easy to encode, the left(the bigger) takes zero always
                n1.b=0
                n2.b=1
                n12.leftnode=n1
                n12.rightnode=n2
            else:
                n1.b=1
                n2.b=0
                n12.leftnode=n2
                n12.rightnode=n1
            hq.heappush(self.H,n12)
    def build_encoding_decoding_dict(self,node,code_text):
        if node.leftnode==None and  node.rightnode==None:#its next isempty, take the code
            self.encoding_dict[node.val]=code_text
            self.decoding_dict[code_text]=node.val
            return
       
        if node==None:#empty
            return
        self.build_encoding_decoding_dict(node.leftnode,code_text+str(node.leftnode.b))#take the left child prefix
        self.build_encoding_decoding_dict(node.rightnode,code_text+str(node.rightnode.b)) #take the right child prefix
        
    def return_encoding_decoding_dict(self):
        node=hq.heappop(self.H)
        self.build_encoding_decoding_dict(node,"")
        return (self.encoding_dict,self.decoding_dict)
            
def pad_encoded_text( encoded_text):
		extra_padding = 8 - len(encoded_text) % 8
		for i in range(extra_padding):
			encoded_text += "0"

		padded_info = "{0:8b}".format(extra_padding)
		encoded_text = padded_info + encoded_text
		return encoded_text     
def Compress(inputpath):
    outputfile_name=str("file")+"Compressed.txt" #make the path in the same file for the sake of implicity
    freq,original_text=Parse(inputpath)
    #print(original_text)
    pr=prob(freq)
    Entropy=0
    for i in pr:
        Entropy+=-1*pr[i]*math.log(pr[i])
    
    
    HT=Huffman_Tree()
    HT.build_heap(freq)
    HT.buid_tree()
    codes_dict,decoding_dict=HT.return_encoding_decoding_dict()
    L=0
    for i in pr:#avg length
        L+=pr[i]*len(codes_dict[i])
    codes_text=""
    for k in original_text:
        codes_text+=codes_dict[k]
 #   print(codes_dict, len(codes_text))
    #print(pad_encoded_text(codes_text),len(pad_encoded_text(codes_text)))
    remaining_bits=8-len(codes_text)%8 #make it divisble by 8
    if(len(codes_text)%8!=0):
       
        remaining_text= "{0:08b}".format(remaining_bits)+"0"*remaining_bits
        codes_text=remaining_text+codes_text
    #print(codes_text,len(codes_text))
    
    codes_bytes=bytearray()
    for i in range(0,len(codes_text),8):
        byte=codes_text[i:i+8]
       # print(byte)
        codes_bytes.append(int(byte,2))#get the byte value from 0 to 255
    #print(codes_bytes)
    with open(outputfile_name, 'wb') as wf: #write as bytes (binary) in the output file
        size= wf.write(bytes(codes_bytes))
  
    
    eff=Entropy/float(L)
    ratio=1-float(L)/8
    return (size,decoding_dict,eff,ratio)
        
def Decompress(path,decoding_dict):
    outputfile_name=str("file")+"Decompressed.txt"
    with open(path, "rb") as rf,open(outputfile_name,'w') as wf:
        #read byte by byte
        encoded_text=""
        byte_read=rf.read(1)
        while len(byte_read) !=0:
            #print(byte_read)
            byte_read = ord(byte_read)#get the ascii code
            byte_read=bin(byte_read)[2:].rjust(8, '0')#convert to string
            encoded_text+=byte_read
            byte_read=rf.read(1)
        bits = encoded_text[:8]
        rem_bits_num = int(bits, 2)
        enoded_text_original = encoded_text[8+rem_bits_num:] 
        #print(enoded_text_original)
        output_text=""
        temp=""
        for C in enoded_text_original:
            temp+=C
            if temp in decoding_dict:
                output_text+=decoding_dict[temp]
                temp=""
        
        wf.write(output_text)
            


choice=int(input("Enter 0 for compression and 1 for decompression: "))

print("the path should be inputed following the format "r"D:\University\Junior\321\Bonus\file.txt"" or just the file name in case it exists in the same folder" ,)
inputpath=input("input path of the file to compress precided by r like in the ex or just the file name: ")
#inputpath=r"D:\University\Junior\321\Bonus\555.txt"
#path=r"D:\University\Junior\321\Bonus"
#filename="555"
if choice==0:
    inputsize = os.path.getsize(inputpath)
    compress_size, decoding_dict,eff,ratio=Compress(inputpath)

    
    W= open("decoding_dict.csv", "w")#store decoding dict
    write_decoding_dict=csv.writer(W)
    for k, v in decoding_dict.items():  
        write_decoding_dict.writerow([k, v])
    W.close()


    compression_ratio=float(compress_size/inputsize)*100
    print("Compression percentage (Compressed size/file size): ",compression_ratio)
    print("Compression Ratio (1-L/8): ",ratio)
    print("efficiency: ",eff)

#print(decoding_dict)
else:
    dec_dict={}
    with open('decoding_dict.csv', 'r') as read_dict:
        reader = csv.reader(read_dict)
        dict_vals=[]
        i=0
        for row in reader:
            #print(row)
            if(i%2==0):#read every two rows
                k=row[0]
                v=row[1]
                dec_dict[k]=v
            i+=1
            
    read_dict.close()
    
    #print(dec_dict)
    #Decompression_Path=r"D:\University\Junior\321\Bonus\555Compressed.txt"
    Decompress(inputpath,dec_dict)
    print("Done Decompressing")





    
    
    
    
    
    

    