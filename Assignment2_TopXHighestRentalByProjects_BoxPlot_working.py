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

#process Data for 1 district
def processData(fdata, startYear, endYear, descending,minArea,maxArea, selectedDistrict,numBedrooms):
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

    print("floor--"*3 + "\n{}".format(fdata['area']))
    
    #filter range of floor area
    fdata = fdata[(fdata['area'] >= minArea) & (fdata['area'] <= maxArea)]
    print("fdataarea--"*3 + "\n{}".format(fdata))
        
    #filter by bedrooms
    if (numBedrooms!=0):
        fdata=fdata[fdata['No. of Bedroom(for Non-Landed Only)']==numBedrooms]
        print("numBedrooms--"*3 + "\n{}".format(fdata))

    print("min--"*3 + "\n{}".format(fdata['area'].min()))
    print("max--"*3 + "\n{}".format(fdata['area'].max()))
    
    #filter by 1 District
    fdata=fdata[fdata['Postal District']==selectedDistrict]
    print("district--"*3 + "\n{}".format(fdata))
    
    allRentByProjects={}
        
    medianRentByProjects=fdata.groupby(['Building/Project Name'])['Monthly Gross Rent($)'].median()
    print("medianRentByProjects--"*3 + "\n{}".format(medianRentByProjects))
    
    medianRentByProjects=medianRentByProjects.sort_values(ascending=False)
    print("medianRentByProjects--"*3 + "\n{}".format(medianRentByProjects))
    print("iloc--"*3 + "\n{}".format(medianRentByProjects.iloc[0]))

    #for every project, get all rent 
    for project in medianRentByProjects.index:
        print("project--"*3 + "\n{}".format(project))
        tmp=fdata[fdata['Building/Project Name']==project]
        #print("tmp--"*3 + "\n{}".format(tmp))

        if (len(tmp)>0):
            rent=tmp['Monthly Gross Rent($)']
            allRentByProjects[project]=(rent)

    print("allRentByProjects--"*3 + "\n{}".format(allRentByProjects))

    return (medianRentByProjects,allRentByProjects,fdata['area'].min(),fdata['area'].max())

#display line chart
def displayBoxPlot(chartData1,chartData2,districtData,startYear,endYear,minFloorArea,maxFloorArea,numBedrooms,numProjects,selectedDistrict):
    print("displayBoxPlot"+"-"*30)
    print("chartData1--"*3 + "\n{}".format(chartData1))
    print("chartData1index--"*3 + "\n{}".format(chartData1.index))
    print("chartData2--"*3 + "\n{}".format(chartData2))
    
    #retrieve district location
    strDistrict="{:0>2}".format(selectedDistrict)
    districtLoc=districtData[districtData['Postal District']==strDistrict]['Locations']

    #xValues.append(districtLoc.index[0])
    districtLoc=strDistrict+"-"+districtLoc.iloc[0]

    print("numBedrooms--"*3 + "\n{}".format(numBedrooms))
    bedroomText=""
    if (numBedrooms!=0):
        bedroomText="{} bedroom(s)".format(numBedrooms)
        print("bedroomText--"*3 + "\n{}".format(bedroomText))
       
    if (startYear==endYear):
        yearText="for {}".format(startYear)
    else:
        yearText="from {} to {}".format(startYear,endYear)

    title = "Non-Landed Private Property Median Rental in {} {} ({} {} - {} sqft)".format(districtLoc,yearText,bedroomText,minFloorArea,maxFloorArea)
    titlelen = len(title)
    print("{:*^{titlelen}}".format(title, titlelen=titlelen+6))
    print()

    plt.figure(2, figsize=(30,30))
    plt.title(title,fontsize=12)
    plt.xlabel('Projects',fontsize=12)
    plt.ylabel('Monthly Gross Rent($)',fontsize=12)
    plt.yticks(fontsize=8)
    plt.xticks(fontsize=6,rotation=10)
    
    labels=[]
    values_combined=[]
    
    compareList=[len(chartData1.index),numProjects]
    projectsToDisplay=min(compareList)
    
    #display Top X only
    for i in range(projectsToDisplay):
        project=chartData1.index[i]
        labels.append(project)
        values_combined.append(chartData2[project])
        
    bp_dict = plt.boxplot(values_combined,labels=labels,patch_artist=True)

    ## change outline color, fill color and linewidth of the boxes
    for box in bp_dict['boxes']:
        # change outline color
        box.set( color='#7570b3', linewidth=2)
        # change fill color
        box.set( facecolor = '#1b9e77' )
        
    ## change color and linewidth of the whiskers
    for whisker in bp_dict['whiskers']:
        whisker.set(color='#7570b3', linewidth=2)
    
    ## change color and linewidth of the caps
    for cap in bp_dict['caps']:
        cap.set(color='#7570b3', linewidth=2)
    
    ## change color and linewidth of the medians
    for median in bp_dict['medians']:
        median.set(color='#b2df8a', linewidth=2)
    
    ## change the style of fliers and their fill
    for flier in bp_dict['fliers']:
        flier.set(marker='D', color='#e7298a', alpha=0.5)
    
    print(bp_dict.keys())
    
    for line in bp_dict['medians']:
        # get position data for median line
        x, y = line.get_xydata()[1] # top of median line
        # overlay median value
        plt.text(x, y, '%.1f' % y,
             horizontalalignment='center',fontsize=10) # draw above, centered
    
    fliers = []
    for line in bp_dict['fliers']:
        ndarray = line.get_xydata()
        if (len(ndarray)>0):
           max_flier = ndarray[:,1].max()
           max_flier_index = ndarray[:,1].argmax()
           x = ndarray[max_flier_index,0]
           print("Flier: " + str(x) + "," + str(max_flier))
         
           plt.text(x,max_flier,'%.1f' % max_flier,horizontalalignment='center',fontsize=10,color='green') 
    
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

startYear=2016
endYear=2020
numProjects=10

bedrooms=0
minFloorArea=750
maxFloorArea=1000

forDistrict=28
avgMedianRentByProjects,allRentByProjects,minFloorArea,maxFloorArea=processData(data1, startYear, endYear, False,minFloorArea,maxFloorArea,forDistrict,bedrooms)
displayBoxPlot(avgMedianRentByProjects,allRentByProjects,districtData,startYear, endYear,minFloorArea,maxFloorArea,bedrooms,numProjects,forDistrict)
#displayLineChart(districtPrice10Y,districtData,numPostalDistricts, startYear, endYear,random.choice(colours),minFloorArea,maxFloorArea)


'''
bedrooms=2
minFloorArea=751
maxFloorArea=1000
selectedDistricts=[14,26,28]

rentData=processData(data1, startYear, endYear, False,minFloorArea,maxFloorArea,forDistrict,bedrooms)
displayBoxPlot(rentData,districtData,startYear, endYear,minFloorArea,maxFloorArea,bedrooms)
'''
print("MAIN END"+"-"*30)

