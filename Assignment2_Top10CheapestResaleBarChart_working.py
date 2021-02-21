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
  
    #print("districtDF--"*3 + "\n{}".format(districtDF))

    return (d,districtDF)


#Median Resale prices by district for a given period (years), sorted ascending/descending
def processData(fdata, startYear, endYear, descending,minArea,maxArea,tenureType):
    print("processData"+"-"*30)

    print("fdata"*3 + "\n{}".format(fdata))

    #create year column - last 2 charactor
    fdata['year'] = "20"+fdata['Date of Sale'].str.slice(-2)
    
    #print("fdata"*3 + "\n{}".format(fdata['year']))
    fdata['year'] = fdata['year'].astype("int32") #convert year to number
    
    #filter for year period
    fdata = fdata[(fdata['year'] >= startYear) & (fdata['year'] <= endYear)]
    
    #filter range of floor area
    fdata = fdata[(fdata['Area (Sqft)'] >= minArea) & (fdata['Area (Sqft)'] <= maxArea)]
    
    #filter by Tenure
    fdata=fdata[fdata['Tenure']==tenureType]

#????
    fdata['Postal District'] = fdata['Postal District'].astype("int32") #convert year to number
    
    #all_districts=np.unique(fdata['Postal District'])
    #print("1--"*3 + "\n{}".format(all_districts))
    
    medianByDistrictYear=fdata.groupby(['Postal District','year'])[['Price ($)']].median()
    #print("medianByDistrictYear--"*3 + "\n{}".format(medianByDistrictYear))
   
    avgMedianByDistrict=medianByDistrictYear.groupby(['Postal District'])[['Price ($)']].mean()
    avgMedianByDistrict=avgMedianByDistrict.sort_values(by="Price ($)")
   
    print("avgMedianByDistrict--"*3 + "\n{}".format(avgMedianByDistrict))
   
    return (avgMedianByDistrict,medianByDistrictYear)

#display the Chart
def displayBarChart(chartData,districtData, numRec, startYear, endYear,colour,minArea,maxArea,tenureType):
        print("displayBarChart"+"-"*30)
        print("chartData--"*3 + "\n{}".format(chartData))
               
        #chart only Top x cheapest
        compareList=[numRec,len(chartData.index)]
        numDistrictsToDisplay=min(compareList)
        #print("numDistrictsToDisplay--"*3 + "\n{}".format(numDistrictsToDisplay))

        #merge to get  district description
        #chartData = pd.concat([chartData, districtData], axis=1)
        #chartData = pd.merge(chartData, districtData, how='inner', on='Postal District')
        #print("lllllll--"*3 + "\n{}".format(districtData[districtData['Postal District']=='10']['Locations']))        
        #print("1mmmm--"*3 + "\n{}".format(chartData.columns))        

        xValues=[]#chartData.index#chartData['Locations']
        yValues=[]

        for i in range(numDistrictsToDisplay):
            #print(i)
            #print("1--"*3 + "\n{}".format(chartData.index[i]))
            #print("1--"*3 + "\n{}".format(chartData.iloc[i,0]))
            
            #get district locations for x-axis
            strDistrict="{:0>2}".format(str(chartData.index[i]))
            districtLoc=districtData[districtData['Postal District']==strDistrict]['Locations']

            #xValues.append(districtLoc.index[0])
            xValues.append(strDistrict+"-"+districtLoc.iloc[0][0:20])
            yValues.append(chartData.iloc[i,0])
            #yValues.append(chartData.iloc[i,1])

        #print("xValues--"*3 + "\n{}".format(xValues))
        #print("yValues--"*3 + "\n{}".format(yValues))
        
        width = 0.8

        loc = np.arange(numDistrictsToDisplay)

        fig, ax = plt.subplots()
        rects1 = ax.bar(loc + width/2, yValues, width, color=colour)

        
        if (startYear==endYear):
            yearText="for {}".format(startYear)
        else:
            yearText="from {} to {}".format(startYear,endYear)

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_xlabel('Postal Districts')
        ax.set_ylabel('Average Median Private Property Prices (Non-Landed)')
        ax.set_title('Top {} Districts with Lowest Prices {} ({} - {} sqft) - {}'.format(numDistrictsToDisplay,yearText,minArea,maxArea,tenureType))
        ax.set_xticks(loc)
        ax.set_xticklabels(xValues, fontsize=8)
        #ax.legend()

        def autolabel(rects):
            """Attach a text label above each bar in *rects*, displaying its height."""
            for rect in rects:
                height = rect.get_height()
                ax.annotate('${:.0f}'.format(height),
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

        #label each bar with the amount
        autolabel(rects1)

        fig.tight_layout()
        
        plt.xticks(loc, xValues, rotation=20)
        
        #plt.savefig('Bar_Top " + numRec+ " Cheapest'+flatType+".png")
        plt.show()

                    
#main
print("MAIN START"+"-"*30)

colours=["green","blue","orange","purple","yellow","indigo"]


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

minFloorArea=500
maxFloorArea=750

numPostalDistricts=10
tenureType='Freehold'

sortAvg10YData,districtPrice10Y=processData(data1, startYear, endYear, False,minFloorArea,maxFloorArea,tenureType)
displayBarChart(sortAvg10YData,districtData,numPostalDistricts, startYear, endYear,random.choice(colours),minFloorArea,maxFloorArea,tenureType)

minFloorArea=751
maxFloorArea=1000

sortAvg10YData,districtPrice10Y=processData(data1, startYear, endYear, False,minFloorArea,maxFloorArea,tenureType)
displayBarChart(sortAvg10YData,districtData,numPostalDistricts, startYear, endYear,random.choice(colours),minFloorArea,maxFloorArea,tenureType)

minFloorArea=1001
maxFloorArea=9999

sortAvg10YData,districtPrice10Y=processData(data1, startYear, endYear, False,minFloorArea,maxFloorArea,tenureType)
displayBarChart(sortAvg10YData,districtData,numPostalDistricts, startYear, endYear,random.choice(colours),minFloorArea,maxFloorArea,tenureType)

print("MAIN END"+"-"*30)

