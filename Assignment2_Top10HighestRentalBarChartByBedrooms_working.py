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

    
    #d['Floor Area (sq ft)'] = pd.to_numeric(d['Floor Area (sq ft)'], errors="coerce") 
    #print("***Floor Area--"*3 + "\n{}".format(d['Floor Area (sq ft)']))

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
def processData(fdata, startYear, endYear, descending,minArea,maxArea, districtList,numBedrooms):
    print("processData"+"-"*30)
    
    print("fdata--"*3 + "\n{}".format(fdata))

    #create year column - last 2 charactor
    print(fdata['Lease Commencement Date'])
    fdata['year'] = fdata['Lease Commencement Date'].str.slice(-4)
    fdata['year'] = fdata['year'].astype("int32") #convert year to number
        
    #filter for year period
    fdata = fdata[(fdata['year'] >= startYear) & (fdata['year'] <= endYear)]
    #print("fdata--"*3 + "\n{}".format(fdata))
   
    fdata['area'] = fdata['area'].astype("int32") #convert year to number

    #print("floor--"*3 + "\n{}".format(fdata['area']))
    
    #filter range of floor area
    fdata = fdata[(fdata['area'] >= minArea) & (fdata['area'] <= maxArea)]
    print("fdataarea--"*3 + "\n{}".format(fdata))
    
    #filter by District
    fdata=fdata[fdata['Postal District'].isin(districtList)]
    #print("districtList--"*3 + "\n{}".format(fdata))
    
    #filter by bedrooms
    if (numBedrooms!=0):
        fdata=fdata[fdata['No. of Bedroom(for Non-Landed Only)']==numBedrooms]
        #print("numBedrooms--"*3 + "\n{}".format(fdata))

    #print("min--"*3 + "\n{}".format(fdata['area'].min()))
    #print("max--"*3 + "\n{}".format(fdata['area'].max()))
    
    medianByDistrictYear=fdata.groupby(['Postal District','year'])[['Monthly Gross Rent($)']].median()
    print("medianByDistrictYear--"*3 + "\n{}".format(medianByDistrictYear))
   
    avgMedianByDistrict=medianByDistrictYear.groupby(['Postal District'])[['Monthly Gross Rent($)']].mean()
    avgMedianByDistrict=avgMedianByDistrict.sort_values(by="Monthly Gross Rent($)",ascending=False)
    print("avgMedianByDistrict--"*3 + "\n{}".format(avgMedianByDistrict))
    
   
    return (avgMedianByDistrict,medianByDistrictYear,fdata['area'].min(),fdata['area'].max())

#display the Chart
def displayBarChart(chartData,districtData, numRec, startYear, endYear,colour,minArea,maxArea,numBedrooms):
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
        rects1 = ax.bar(loc+width/2, yValues, width, color=colour)

        print("numBedrooms--"*3 + "\n{}".format(numBedrooms))
        bedroomText=""
        if (numBedrooms!=0):
            bedroomText="{} bedroom(s)".format(numBedrooms)
        #print("bedroomText--"*3 + "\n{}".format(bedroomText))
       
        if (startYear==endYear):
            yearText="for {}".format(startYear)
        else:
            yearText="from {} to {}".format(startYear,endYear)

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_xlabel('Postal Districts')
        ax.set_ylabel('Average Median Rental')
        ax.set_title('Average Median Private Property Rental (Non-Landed) {} ({} {} - {} sqft)'.format(yearText,bedroomText,minArea,maxArea))
        ax.set_xticks(loc)
        ax.set_xticklabels(xValues,fontsize=8)
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

colours=["red","green","blue","orange","yellow","purple"]

fileDir="data/rental/"

'''
startYear=int(input("Please Enter the Start Year of data to analyse: "))
endYear=int(input("Please Enter the Start Year of data to analyse: "))

minFloorArea=int(input("Please Enter the Minimum Floor Area : "))
maxFloorArea=int(input("Please Enter the Maximum Floor Area : "))

numPostalDistricts=int(input("How many districts do you want to display? "))
'''
startYear=2020
endYear=2020

numPostalDistricts=10

selectedDistricts=[14,15,12,26,5,3,13,8,23]

(data1,districtData)=extractData(fileDir)

bedrooms=0
minFloorArea=500
maxFloorArea=750
sortAvg10YData,districtPrice10Y,minFloorArea,maxFloorArea=processData(data1, startYear, endYear, False,minFloorArea,maxFloorArea,selectedDistricts,bedrooms)
displayBarChart(sortAvg10YData,districtData,numPostalDistricts, startYear, endYear,random.choice(colours),minFloorArea,maxFloorArea,bedrooms)
#displayLineChart(districtPrice10Y,districtData,numPostalDistricts, startYear, endYear,random.choice(colours),minFloorArea,maxFloorArea)

bedrooms=0
minFloorArea=751
maxFloorArea=1000
selectedDistricts=[14,26,28]

sortAvg10YData,districtPrice10Y,minFloorArea,maxFloorArea=processData(data1, startYear, endYear, False,minFloorArea,maxFloorArea,selectedDistricts,bedrooms)
displayBarChart(sortAvg10YData,districtData,numPostalDistricts, startYear, endYear,random.choice(colours),minFloorArea,maxFloorArea,bedrooms)

print("MAIN END"+"-"*30)

