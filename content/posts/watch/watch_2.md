
Title: Apple Health Data Analysis Series - First Looks
Date: 2022-05-13 11:30:00
Category: posts
Tags: Data Watch
author: Dane Collins
Summary: How can you do your own data analysis on Apple Health Data


In this post we'll take a look at what is in the data we received from the Health app.

## Overview

#### Expanding the Data

Once you have the data on your computer you will notice that it is a ZIP Archive and needs to be expanded.  When expanded, the data will create a directory named **apple_health_export** that contains:

* export.xml: this is the data file we will be using.
* export_cda.xml: this contains a subset of the data in export.xml so it is not needed.
* workout-routes/: these are **GPX** formatted files of the routes captured during excersize events.  We will not analyze these.
* eletrocardiograms/: these are **CSV** files of the captured electrocardiograms.

#### Digging into export.xml

There is a huge amount of information in the XML file and it is useful to understand some of the basics as they will be useful when we analyze the data.

The first hundred of so lines of the file explain what fields can exist in the file.  Once we're past that, all the data is in **Record** fields. 

##### Record field

The first field in the record is **type** which indicates what data is in the record.  There are a large number of these including types like:


* HKQuantityTypeIdentifierHeartRate
* HKQuantityTypeIdentifierRestingHeartRate
* HKQuantityTypeIdentifierEnvironmentalAudioExposure
* HKQuantityTypeIdentifierHeadphoneAudioExposure
* HKQuantityTypeIdentifierBloodPressureSystolic
* HKQuantityTypeIdentifierBloodPressureDiastolic
* HKQuantityTypeIdentifierStepCount
* HKQuantityTypeIdentifierDistanceWalkingRunning
* HKQuantityTypeIdentifierDistanceCycling
* HKQuantityTypeIdentifierVO2Max
* HKQuantityTypeIdentifierFlightsClimbed
* HKQuantityTypeIdentifierAppleStandTime
* HKCategoryTypeIdentifierAppleStandHour
* HKQuantityTypeIdentifierHeartRateVariabilitySDNN
* HKQuantityTypeIdentifierWalkingHeartRateAverage
* HKQuantityTypeIdentifierBasalEnergyBurned
* HKQuantityTypeIdentifierActiveEnergyBurned
* HKQuantityTypeIdentifierAppleExerciseTime'

Each record field will have a **creationDate**, a **startDate** and an **endDate** even if the data is a measurement at a single point in time.

The record field will have a **sourceName** which is the device or application that created the record. This field can be very useful since some record types can be collected from multiple devices.  For example, StepCount can be collected by an iPhone and an Apple Watch.  When displaying steps, the Health and Fitness apps will attempt to merge this data but it is kept separate in the export.xml.

**Note:** I have found that the merging of phone and watch step data can lead to significant over-estimation of steps.  By using the raw data in the export.xml you can keep these values separate.

The data value is in a **value** field with the unit name for the field being in a **unit** field.

Some records will also have a **device** field which contains information about the hardware that generated the record.

If you are only interested in performing data analysis on the basic information types (steps for example) you do not need to understand the format of the XML file as I will provide parsers to extract that data and you can skip to the next blog post.

The rest of this post will go into some of the details of the XML file. I won't cover each type individually as you will see they are all quite similar in structure.

## Details

Once unpacked from the ZIP file you will note that the export.xml is quite large.  In my case the files has almost 8M lines.

#### Heart Rate

Here is a typical Heart Rate record

```
 <Record type="HKQuantityTypeIdentifierHeartRate" 
         sourceName="Dane’s Apple Watch" 
         sourceVersion="7.6.2" 
         device="&lt;&lt;HKDevice: 0x280bec690&gt;, name:Apple Watch, manufacturer:Apple Inc., model:Watch, hardware:Watch5,4, software:7.6.2&gt;" 
         unit="count/min" 
         creationDate="2021-09-25 16:31:44 -0700" 
         startDate="2021-09-25 16:30:38 -0700" 
         endDate="2021-09-25 16:30:38 -0700" 
         value="53.0572">
  <MetadataEntry key="HKMetadataKeyHeartRateMotionContext" 
                 value="0"/>
 </Record>
 ```

A few things to note here.  The value is usually an integer if captured by the heart rate app.  The ECG app computes an average heart rate over the ECG and stores a floating point value.

There is additional data in the record for the motion context but I can only guess at what its value means.

#### Distance

Here is a typical distance record.

```
 <Record type="HKQuantityTypeIdentifierDistanceWalkingRunning" 
         sourceName="Dane’s Apple Watch" 
         sourceVersion="7.5" device="&lt;&lt;HKDevice: 0x280830410&gt;, name:Apple Watch, manufacturer:Apple Inc., model:Watch, hardware:Watch5,4, software:7.5&gt;" 
         unit="mi" 
         creationDate="2021-06-11 15:12:30 -0700" 
         startDate="2021-06-11 15:12:16 -0700" 
         endDate="2021-06-11 15:12:26 -0700" 
         value="0.0111951"/>
 ```
 
The main thing to note is that the intevals for these records will vary. To get daily totals these value need to be summed by date.
 
#### Energy

Here is a typical energy record.

```
 <Record type="HKQuantityTypeIdentifierBasalEnergyBurned" 
         sourceName="Dane’s Apple Watch" 
         sourceVersion="6.2.5" device="&lt;&lt;HKDevice: 0x280bee6c0&gt;, name:Apple Watch, manufacturer:Apple Inc., model:Watch, hardware:Watch5,4, software:6.2.5&gt;" 
         unit="Cal" 
         creationDate="2020-05-29 12:33:00 -0700" 
         startDate="2020-05-29 12:14:17 -0700" 
         endDate="2020-05-29 12:28:08 -0700" 
         value="20.487"/>
```

Again the intevals for these records will vary. To get daily totals these value need to be summed by date.


#### Flights Climbed

Here is the sample record for flights of stairs climbed

```
Record type="HKQuantityTypeIdentifierFlightsClimbed" sourceName="Dxi" sourceVersion="12.0" device="&lt;&lt;HKDevice: 0x28222b5c0&gt;, name:iPhone, manufacturer:Apple, model:iPhone, hardware:iPhone10,4, software:12.0&gt;" unit="count" creationDate="2018-10-10 16:40:26 -0700" startDate="2018-10-10 16:25:48 -0700" endDate="2018-10-10 16:26:05 -0700" value="1"/>
```


## Converting the Data

While there are ways to use the XML data directly I find it too large to work with easily.  I also find that I am usually working on analyzing only a couple of metrics at a time and having them separated into individual data sets is more convenient.

In the next post I'll cover using a Python script to convert the data into separate data files.
