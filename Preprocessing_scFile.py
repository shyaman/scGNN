#Used for generate sci-CAR and other data to the data format we used
#Original: line as the gene, column as the cell, first column is the gene name, first line is the cell name
#Output:   line as the cell, column as the gene, first line is the gene name.
#
#Usage:
#python Preprocessing_scFile.py --inputfile /home/wangjue/biodata/scData/scRNA_And_scATAC_Files/Processed_Data/GeneSymbolMat.txt\
#--outputfile /home/wangjue/biodata/scData/sci-CAR.csv --outputfileCellName /home/wangjue/biodata/scData/sci-CAR.cellname.txt\
#--cellcount 1414 --genecount 25178 --split space --cellheadflag True
#
#python Preprocessing_scFile.py --inputfile /home/wangjue/biodata/scData/scRNA_And_scATAC_Files/Processed_Data/GeneSymbolMat.dic\
#--outputfile /home/wangjue/biodata/scData/sci-CAR_LTMG.csv --outputfileCellName /home/wangjue/biodata/scData/sci-CAR.cellname.txt\
#--cellcount 1414 --genecount 19467 --split space --cellheadflag True
#
# Benchmark:
# python Preprocessing_scFile.py --inputfile /home/wangjue/biodata/scData/AnjunBenchmark/1.Biase/Biase_expression.csv --outputfile /home/wangjue/biodata/scData/1.Biase.csv --outputfileCellName /home/wangjue/biodata/scData/1.Biase.cellname.txt --cellcount 49 --genecount 25737 --split dot --cellheadflag False
# python Preprocessing_scFile.py --inputfile /home/wangjue/biodata/scData/AnjunBenchmark/2.Yan/Yan_expression.csv --outputfile /home/wangjue/biodata/scData/2.Yan.csv --outputfileCellName /home/wangjue/biodata/scData/2.Yan.cellname.txt --cellcount 90 --genecount 20214 --split dot --cellheadflag False
# python Preprocessing_scFile.py --inputfile /home/wangjue/biodata/scData/AnjunBenchmark/3.Goolam/Goolam_expression.csv --outputfile /home/wangjue/biodata/scData/3.Goolam.csv --outputfileCellName /home/wangjue/biodata/scData/3.Goolam.cellname.txt --cellcount 124 --genecount 41480 --split dot --cellheadflag False
# python Preprocessing_scFile.py --inputfile /home/wangjue/biodata/scData/AnjunBenchmark/4.Deng/Deng_expression.csv --outputfile /home/wangjue/biodata/scData/4.Deng.csv --outputfileCellName /home/wangjue/biodata/scData/4.Deng.cellname.txt --cellcount 268 --genecount 22457 --split dot --cellheadflag False
# python Preprocessing_scFile.py --inputfile /home/wangjue/biodata/scData/AnjunBenchmark/5.Pollen/Pollen_expression.csv --outputfile /home/wangjue/biodata/scData/5.Pollen.csv --outputfileCellName /home/wangjue/biodata/scData/5.Pollen.cellname.txt --cellcount 301 --genecount 23730 --split dot --cellheadflag False
# python Preprocessing_scFile.py --inputfile /home/wangjue/biodata/scData/AnjunBenchmark/6.Kolodziejczyk/Kolodziejczyk_expression.csv --outputfile /home/wangjue/biodata/scData/6.Kolodziejczyk.csv --outputfileCellName /home/wangjue/biodata/scData/6.Kolodziejczyk.cellname.txt --cellcount 704 --genecount 38653 --split dot --cellheadflag False


import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--inputfile', type=str, default='/home/wangjue/biodata/scData/scRNA_And_scATAC_Files/Processed_Data/GeneSymbolMat.dic',
                    help='inputfile name')
parser.add_argument('--outputfile', type=str, default='/home/wangjue/biodata/scData/sci-CAR_LTMG.csv',
                    help='outputfile name')
parser.add_argument('--outputfileCellName', type=str, default='/home/wangjue/biodata/scData/sci-CAR.cellname.txt',
                    help='outputfile cell name')
parser.add_argument('--cellcount', type=int, default=1414,
                    help='total cell count')
parser.add_argument('--genecount', type=int, default=19467,
                    help='total gene count')
parser.add_argument('--split', type=str, default='space',
                    help='dot/blank')
parser.add_argument('--cellheadflag', type=bool, default=False,
                    help='True/False')
args = parser.parse_args()

# Original
# # inputfile  = '/home/wangjue/biodata/scData/scRNA_And_scATAC_Files/Processed_Data/GeneSymbolMat.txt'
# # outputfile = '/home/wangjue/biodata/scData/sci-CAR.csv'
# inputfile  = '/home/wangjue/biodata/scData/scRNA_And_scATAC_Files/Processed_Data/GeneSymbolMat.dic'
# outputfile = '/home/wangjue/biodata/scData/sci-CAR_LTMG.csv'
# outputfileCellName = '/home/wangjue/biodata/scData/sci-CAR.cellname.txt'
# cellcount = 1414
# # Original:
# genecount = 25178
# # Discretization:
# # genecount = 19467

inputfile = args.inputfile
outputfile = args.outputfile
outputfileCellName = args.outputfileCellName
cellcount = args.cellcount
genecount = args.genecount
splitChar = ''
if args.split == 'space':
    splitChar = ''
elif args.split == 'dot':
    splitChar = ',' 

cellNames = []
geneNamesLine = ''

#cell as the row, col as the gene
contentArray = [[0.0] * genecount for i in range(cellcount)]
contentArray = np.asarray(contentArray)

count = -1
with open(inputfile, 'r') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        if splitChar == '':
            words = line.split()
        else:
            words = line.split(splitChar)
        if count == -1:
            colcount = -1
            for word in words:
                if args.cellheadflag or colcount > -1:
                    cellNames.append(word)
                colcount += 1
        else:
            colcount = -1
            for word in words:
                if colcount == -1:
                    geneNamesLine = geneNamesLine + word + ','
                else:
                    contentArray[colcount,count] = word
                colcount+=1
        count += 1
    f.close()

with open(outputfile, 'w') as fw:
    fw.write(geneNamesLine+'\n')
    for i in range(contentArray.shape[0]):
        for j in range(contentArray.shape[1]):
            fw.write(str(contentArray[i][j])+',')
        fw.write('\n')
    fw.close()

with open(outputfileCellName, 'w') as fw:
    for cell in cellNames:
        fw.write(str(cell)+'\n')
    fw.close()