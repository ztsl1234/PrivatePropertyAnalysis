# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 22:26:15 2020

@author: admin

TOP 10 CHEAPEST RESALE PROPERTY  (bar chart)

"""
import numpy as np
import matplotlib.pyplot as plt

import  pandas as pd
import random
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
    print(fdata['Price ($)'].describe())

    
#Extract Data
def extractData(dir):
    print("extractData"+"-"*30)
    
    mainDf={}
    
    with os.scandir(dir) as fileList:
        for file in fileList:
            print(file.name)
            df=pd.read_csv(dir+file.name)
            print("Successfully loaded dataset {}".format(file.name))
            print("Merging data"+"-"*30)
            if (len(mainDf)==0):
                mainDf=df
            else:
                mainDf=pd.concat([mainDf, df])
    
    print("***99--"*3 + "\n{}".format(mainDf))
    
    d=mainDf
    #print(d)
    textBasedAnalysis(d)

    #Data Cleaning
    
    #convert price to numeric - ignore all errors i.e. all non numbers will become NaN
    d['Price ($)'] = pd.to_numeric(d['Price ($)'], errors="coerce")
    d['Area (Sqft)'] = pd.to_numeric(d['Area (Sqft)'], errors="coerce") 
    d['Unit Price ($psf)'] = pd.to_numeric(d['Unit Price ($psf)'], errors="coerce") 
    #d['Postal District'] = pd.to_numeric(d['Postal District'], errors="coerce") 

    #print("***d--"*3 + "\n{}".format(d))

     #check rows with NA
    print("***isnull--"*3 + "\n{}".format(pd.isnull(d['Price ($)'])))
    print("***99null--"*3 + "\n{}".format(d[pd.isnull(d['Area (Sqft)'])])) 
    print("***99null--"*3 + "\n{}".format(d[pd.isnull(d['Unit Price ($psf)'])])) 


    #remove rows with missing value
    d = d.dropna()
    #d = d.fillna(0)
    print("***fillna--"*3 + "\n{}".format(len(d)))

    #load district code description
    districtDF= pd.read_html('https://www.ura.gov.sg/realEstateIIWeb/resources/misc/list_of_postal_districts.htm')[0]

    #print("districtDF--"*3 + "\n{}".format(districtDF))
    #print("districtDF--"*3 + "\n{}".format(type(districtDF)))
    #print("districtDF--"*3 + "\n{}".format(districtDF[0]))#Postal District
    #print("districtDF--"*3 + "\n{}".format(districtDF[1]))#Postal Sector
    #print("districtDF--"*3 + "\n{}".format(districtDF[2]))#Description
    
    #add new cols cos read from html do not create the column names
    districtDF['Postal District']=districtDF[0]
    districtDF['Locations']=districtDF[2]
    
    #print("districtDF--"*3 + "\n{}".format(districtDF))
    
    #clean spaces in Locations
    districtDF['Locations']=districtDF['Locations'].str.replace(", ",",")
  
    print("districtDF--"*3 + "\n{}".format(districtDF))

    return (d,districtDF)


#Median Resale prices by district for a given period (years), sorted ascending/descending
def processData(fdata, startYear, endYear, descending,minArea,maxArea,tenureType):
    print("processData"+"-"*30)

    print("fdata"*3 + "\n{}".format(fdata))

    #create year column - last 2 charactor
    fdata['year'] = "20"+fdata['Date of Sale'].str.slice(-2)
    
    print("fdata"*3 + "\n{}".format(fdata['year']))
    fdata['year'] = fdata['year'].astype("int32") #convert year to number
    
    #filter for year period
    fdata = fdata[(fdata['year'] >= startYear) & (fdata['year'] <= endYear)]
    
    #filter range of floor area
    fdata = fdata[(fdata['Area (Sqft)'] >= minArea) & (fdata['Area (Sqft)'] <= maxArea)]
    
    #filter by Tenure
    fdata=fdata[fdata['Tenure']==tenureType]

#????
    fdata['Postal District'] = fdata['Postal District'].astype("int32") #convert year to number
    
    transNum=fdata['Price ($)'].count()
    print("transNum--"*3 + "\n{}".format(transNum))
 
    return (transNum)

#display the Chart
def displayPieChart(chartData,startYear, endYear,tenureType):
        print("displayBarChart"+"-"*30)
        print("chartData--"*3 + "\n{}".format(chartData))
               
               
        if (startYear==endYear):
            yearText="for {}".format(startYear)
        else:
            yearText="from {} to {}".format(startYear,endYear)

        fig, ax = plt.subplots()

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_title('Sale Transactions By Floor Area {} - {}'.format(yearText,tenureType))
        ax.pie(chartData.values(), labels = chartData.keys(), shadow = True,autopct='%1.1f%%')
        
        ax.legend(loc='lower left')

        fig.tight_layout()
                
        #plt.savefig('Bar_Top " numRec+ " Cheapest'+flatType+".png")
        plt.show()

                    
#main
print("MAIN START"+"-"*30)

colours=["red","green","blue","orange","yellow","purple"]


fileDir="data/resalePrices/"

'''
startYear=int(input("Please Enter the Start Year of data to analyse: "))
endYear=int(input("Please Enter the Start Year of data to analyse: "))

minFloorArea=int(input("Please Enter the Minimum Floor Area : "))
maxFloorArea=int(input("Please Enter the Maximum Floor Area : "))

numPostalDistricts=int(input("How many districts do you want to display? "))
'''

(data1,districtData)=extractData(fileDir)

startYear=2020
endYear=2020

tenureType='Freehold'
dataForChart={}

floorAreaList=[(0,499),(500,750),(751,1000),(1001,9999)]

for area in floorAreaList:
    print("area--"*3 + "\n{}".format(area))
    numTrans=processData(data1, startYear, endYear, False,area[0],area[1],tenureType)
    dataForChart[str(area[0])+"-"+str(area[1])]=numTrans

displayPieChart(dataForChart,startYear, endYear,tenureType)

print("MAIN END"+"-"*30)

