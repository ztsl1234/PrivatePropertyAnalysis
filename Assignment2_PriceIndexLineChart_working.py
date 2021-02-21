S# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 22:26:15 2020

@author: admin

Private Property Residential (Non-Landed) Price Index By localities By Year

"""
import numpy as np
import matplotlib.pyplot as plt

import  pandas as pd
import os


def textBasedAnalysis(fdata):
    print("textBasedAnalysis"+"-"*30)
    
    print("\nThis is the shape of the dataset")
    print(fdata.shape)
    
    print("\nThis is the index of the dataset")
    print(fdata.index)
    
    print("\nThese are the columns in the dataset")
    print(fdata.columns)
        
    print("\nThe total number of non-NA in this dataset is:")
    print(fdata.count())
    
    print("\nA summary of this dataset is shown below:")
    print(fdata.info())
    
    print("\nA descriptive statistical summary of this dataset is shown below:")
    print(fdata['price_index'].describe())

    
#Extract Data
def extractData(dir):
    print("extractData"+"-"*30)
    #print("***dir--"*10 + "\n{}".format(dir))
    
    mainDf={}
    
    with os.scandir(dir) as fileList:
        for file in fileList:
            print(file.name)
            df=pd.read_csv(dir+file.name)
            print("Successfully loaded dataset {}".format(file.name))
            if (len(mainDf)==0):
                mainDf=df
            else:
                mainDf=pd.concat([mainDf, df])
    
    print("***99--"*10 + "\n{}".format(mainDf))
    
    d=mainDf
    #print(d)
    textBasedAnalysis(d)

    #Data Cleaning
    
    #convert to numeric - ignore all errors i.e. all non numbers will become NaN
    d['price_index'] = pd.to_numeric(d['price_index'], errors="coerce")

    #print("***d--"*10 + "\n{}".format(d))
    
    #check rows with NA
    print("***isnull--"*10 + "\n{}".format(pd.isnull(d['price_index'])))

    #fill missing value with 0
    #d = d.dropna()
    d = d.fillna(0)
    print("***fillna--"*10 + "\n{}".format(len(d)))
    
    return (d)

def processData(fdata, startYear, endYear):
    print("processData"+"-"*30)
    
    print("fdata"*10 + "\n{}".format(fdata))

    #create year column - last 2 charactor

    fdata['year'] = fdata['quarter'].str.slice(0,4)
    fdata['year'] = fdata['year'].astype("int32") #convert year to number
    
    #filter for year period
    fdata = fdata[(fdata['year'] >= startYear) & (fdata['year'] <= endYear)]
    #print("1YEAR--"*10 + "\n{}".format(fdata))
    
    localities=fdata['market_segment']
    allLocalities=np.unique(localities)
    
    meanIndexByLocalityYear={}
    
    #get index by locality
    for locality in allLocalities:
          #filter for locality
          temp=fdata[fdata['market_segment']==locality]
          meanIndexByLocalityYear[locality]=temp.groupby(['year'])[['price_index']].mean()
        
    #print("meanIndexByLocalityYear--"*10 + "\n{}".format(medianByLocalityYear))
   
    return (meanIndexByLocalityYear)

#display line chart
def displayLineChart(chartData):
    print("displayLineChart"+"-"*30)
    
    print("chartData--"*10 + "\n{}".format(chartData))  

    title = "Private Property Price Index of Non-landed Residential Properties by Locality"
    titlelen = len(title)
    print("{:*^{titlelen}}".format(title, titlelen=titlelen+6))
    print()

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
   
    #chartData1=chartData[chartData['locality']=="Whole Island"]
    #print("iloc--"*10 + "\n{}".format(chartData.iloc[:,0]))  
    
    for rec in chartData:
        print(type(chartData[rec]))
        print(chartData[rec])
        ax1.plot(chartData[rec], label=rec, marker="o")
        
    #loc = np.arange(len(chartData[rec]))
    #plt.xticks(loc, len(chartData[rec]), rotation=30)
 
    # Add some text for labels, title and custom x-axis tick labels, etc.
    plt.xlabel('Years')
    plt.ylabel('Price Index')
    plt.title(title)
 
    plt.legend();

    #plt.savefig('Line_'+flatType+".png")
    
    plt.show()
    
#main
print("MAIN START"+"-"*30)

#colours=["red","green","blue","orange","yellow","purple"]
fileDir="data/priceIndex/"

'''
startYear=int(input("Please Enter the Start Year of data to analyse: "))
endYear=int(input("Please Enter the Start Year of data to analyse: "))
'''

data1=extractData(fileDir)

#all data
startYear=1900
endYear=2020

priceIndexByYear=processData(data1, startYear, endYear)
displayLineChart(priceIndexByYear)
