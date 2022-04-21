#!/usr/bin/env python
"""Filter an image collection by date and region to make a median composite.
See also: Clipped composite, which crops the output image
instead of filtering the input collection.
"""

import datetime
import ee
import ee.mapclient
import geetools


ee.Initialize()
StartDate= ee.Date("2020-11-10")
EndDate = ee.Date("2020-11-20")
# Filter to only include images within the bay of honduras boundaries.
polygon = ee.Geometry.Polygon([[-88.956, 17.073],[-86.243, 17.073], [-88.956, 15.671], [-86.243, 15.671]])
# (15.6691, 37.9764) #lt
# (16.1038, 37.9759), #rt
# (15.6698, 37.847), #ll
# (16.1058, 37.8486) #rl
#hondourus
#      long, lat
# lt -88.956, 17.073,
# rt -86.243, 17.073
# ll -88.956, 15.671
# rl -86.243, 15.671,
# Create a Landsat 7 composite for Spring of 2000, and filter by
# the bounds of the FeatureCollection.
collection = (ee.ImageCollection('COPERNICUS/S2_SR')
              .filterDate(StartDate, EndDate)
              .filterBounds(polygon))
count = collection.size()
print(count)
# # Select the median pixel.
# image1 = collection.median()
bands = ['B1','B2','B3','B4','B5','B6','B7','B8','B8A','B11','B12']
data_type = 'float32'
name_pattern = '{system_date}'
date_pattern = 'yMMdd' # dd: day, MMM: month (JAN), y: year
scale = 5
folder_name = './GEE_H'

tasks = geetools.batch.Export.imagecollection.toDrive(
            collection=collection,
            folder=folder_name ,
            region=polygon,
            namePattern=name_pattern,
            scale=scale,
            datePattern=date_pattern,
            verbose=True,
            maxPixels=1e13
        )