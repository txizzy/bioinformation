# -*- coding: utf-8 -*-
import os 
import sys
import argparse
import pandas as pd

#############################################################################
#Author：Xizzy   email: txizzy#gmail.com
#Describtion: Transform ID from GTF file
#Version: V1.0
#Date: 2021/8/28
#Motify:2021/9/5
#Example: python TransFromGTF.py -input CAP-vs-CA.genes.filter.annot.xls -source gene_id -to gene_name -idname id -outname list.out --header
#############################################################################

parser=argparse.ArgumentParser(description='Transform ID from GTF file! This is a type GTF annot: gene_id "ENSG00000187634"; transcript_id "ENST00000342066"; gene_name "SAMD11"; transcript_name "SAMD11-010"; transcript_biotype "protein_coding"; tag "CCDS"; ccds_id "CCDS2"; havana_transcript "OTTHUMT00000276866";tag "basic"')
parser.add_argument('-input',type=str,help='Input file',required=True)
parser.add_argument('-gtf',type=str,help='Your GTF file path",required=True)
parser.add_argument('-outname',type=str,help='Output name, default is out.xls',default='out.xls')
parser.add_argument('-source',type=str,help='Iuput file id type, the name must be same for gtf file!',required=True)
parser.add_argument('-to',type=str,help='The type to be converted, the name must be same for gtf file!',required=True)
parser.add_argument('-idname',type=str,help='Input the name of column to be handled. For no header input, use 0~n to select the column',required=True)
parser.add_argument('--header',action="store_true",help='Input has header')
parser.add_argument('--keep',action="store_true",help='Do not substitute directly')
args=parser.parse_args()


def get_id(id_list,id_from,trans_to):
    with open(args.gtf,'r') as gff:
        result = []
        hash_dict = dict()
        for line in gff:
            line1=line.strip().split('\t',8)
            try:
                Name = line1[8]
            except:
                continue
            try:
                from_type = eval(Name.split(id_from)[1].split(';')[0])
                #hash methods, it need a large memory!!
                to_type = eval(Name.split(trans_to)[1].split(';')[0])
                hash_dict[from_type] = to_type
                #order methods, to slow
                #if from_type in id_list :
                #    to_type = eval(Name.split(trans_to)[1].split(';')[0])
                #    result.append(to_type)
                #    id_list.remove(from_type)
            except:
                continue
        for item in id_list:
            try:
                result.append(hash_dict[item])
            except:
                result.append('')
                continue
        return(result)
if __name__=='__main__':
    if(args.header):
        df = pd.read_csv(args.input,sep='\t')
    else:
        df = pd.read_csv(args.input,sep='\t',header=None)
        args.idname = int(args.idname)
    if(args.source == 'transcript_id'):
        keyword=list(df[args.idname].str.split('.',expand=True)[0])
    else:  
        keyword = list(df[args.idname])
    df.rename(columns={args.idname:args.to},inplace=True)
    if(args.keep):
        df[args.idname] = keyword
    df[args.to] = get_id(keyword,args.source,args.to)
    if(args.header):
        df.to_csv(args.outname,sep='\t',index=0)
    else:
        df.to_csv(args.outname,sep='\t',index=0,header=False)
