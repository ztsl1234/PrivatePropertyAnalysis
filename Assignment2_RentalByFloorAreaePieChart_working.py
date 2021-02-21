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
    print(fdata['Monthly Gross Rent($)'].describe())

    
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
    d['Monthly Gross Rent($)'] = pd.to_numeric(d['Monthly Gross Rent($)'], errors="coerce")
    d['No. of Bedroom(for Non-Landed Only)']= pd.to_numeric(d['No. of Bedroom(for Non-Landed Only)'], errors="coerce")

   #d['Postal District'] = pd.to_numeric(d['Postal District'], errors="coerce") 
    #print("***d--"*3 + "\n{}".format(d))
    
    #create area column 
    #can be >,<,>=,<= 300 --> remove all the symbol and space
    #can be a range --> take- lower vallue of the given floor area range

    #remove the >,<,>=,<=
    #d['area'] = d['Floor Area (sq ft)'].str.slice(0,4)
    #d['area'] =d['Floor Area (sq ft)'].str.split(pat="/")
    #d['area'] =d['Floor Area (sq ft)'].str.split(r"\>=|<=| to ")
    #d['area'] =d['Floor Area (sq ft)'].str.split(pat=" to ")
    d['area'] =d['Floor Area (sq ft)'].str.lstrip('>=<=>< ')
    ##d['area'] =d['area'].str.split(pat=" to ")
    
    d['area'] =d['area'].str.slice(0,4)
    print("**area--"*3 + "\n{}".format(d['area']))   

    d['area'] = pd.to_numeric(d['area'], errors="coerce")

   
    #check rows with NA
    print("***99null--"*3 + "\n{}".format(d[pd.isnull(d['Monthly Gross Rent($)'])]))
    print("***99null--"*3 + "\n{}".format(d[pd.isnull(d['Floor Area (sq ft)'])])) 
    print("***99null--"*3 + "\n{}".format(d[pd.isnull(d['Postal District'])])) 
    print("***99null--"*3 + "\n{}".format(d[pd.isnull(d['No. of Bedroom(for Non-Landed Only)'])])) 
    print("***99null--"*3 + "\n{}".format(d[pd.isnull(d['area'])])) 


    
    #remove rows with missing value
    #d = d.dropna()
    d = d.fillna(0)
    print("***len(d)--"*3 + "\n{}".format(len(d)))
   
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
def processData(fdata, startYear, endYear, descending,minArea,maxArea):
    print("processData"+"-"*30)

    print("fdata"*3 + "\n{}".format(fdata))

    #create year column - last 2 charactor
    #create year column - last 2 charactor
    print(fdata['Lease Commencement Date'])
    fdata['year'] = fdata['Lease Commencement Date'].str.slice(-4)
    fdata['year'] = fdata['year'].astype("int32") #convert year to number
    
    #filter for year period
    fdata = fdata[(fdata['year'] >= startYear) & (fdata['year'] <= endYear)]
    
    #filter range of floor area
    fdata = fdata[(fdata['area'] >= minArea) & (fdata['area'] <= maxArea)]
    print("fdataarea--"*3 + "\n{}".format(fdata))
    
    #filter by bedrooms
    #fdata=fdata[fdata['No. of Bedroom(for Non-Landed Only)']==numBedrooms]
    #print("numBedrooms--"*3 + "\n{}".format(fdata))

    #print("min--"*3 + "\n{}".format(fdata['area'].min()))
    #print("max--"*3 + "\n{}".format(fdata['area'].max()))

#????
    fdata['Postal District'] = fdata['Postal District'].astype("int32") #convert year to number
    
    transNum=fdata['Monthly Gross Rent($)'].count()
    #print("transNum--"*3 + "\n{}".format(transNum))
 
    return (transNum)

#display the Chart
def displayPieChart(chartData,startYear, endYear):
        print("displayBarChart"+"-"*30)
        print("chartData--"*3 + "\n{}".format(chartData))
               
               
        if (startYear==endYear):
            yearText="for {}".format(startYear)
        else:
            yearText="from {} to {}".format(startYear,endYear)

        fig, ax = plt.subplots()

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_title('Rental Contracts By Floor Area {}'.format(yearText))
        ax.pie(chartData.values(), labels = chartData.keys(), shadow = True, autopct='%1.1f%%')
        
        ax.legend(loc='lower left')

        fig.tight_layout()
                
        #plt.savefig('Bar_Top " numRec+ " Cheapest'+flatType+".png")
        plt.show()

                    
#main
print("MAIN START"+"-"*30)

colours=["red","green","blue","orange","yellow","purple"]


fileDir="data/rental/"

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

dataForChart={}

floorAreaList=[(0,499),(500,750),(751,1000),(1001,9999)]

for area in floorAreaList:
    print("area--"*3 + "\n{}".format(area))
    numTrans=processData(data1, startYear, endYear, False,area[0],area[1])
    dataForChart[str(area[0])+"-"+str(area[1])]=numTrans

displayPieChart(dataForChart,startYear, endYear)

print("MAIN END"+"-"*30)

