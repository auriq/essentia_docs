***********************
Category Rules
***********************

Category Name
---------------
The category name can be any name you want to use to group your files. However, it **cannot contain any spaces** and there **cannot be repeat names**. 

Pattern
---------------
This is a UNIX-style globular matching pattern to describe what types of files to include in your category. You can use a series of literal characters combined with wildcards to tell Essentia that any filenames that match this pattern belong in this category.

**Example Patterns:** ::
    
    diy_woodworking/*purchase*
    *store*sales*
    *.dat
    *.csv.gz
    *pagecounts*2009*.gz

..        accesslogs/1*
..        diy_woodworking/*browse*
..        etldata/five*csv
..        etldata/*MOCK*csv

*Note:* For a more detailed description of globular matching patterns, see `Glob (programming) <http://en.wikipedia.org/wiki/Glob_%28programming%29>`_

Comment
---------------
This field can contain any character and is just used to help you make notes about your categories or the files the contain.

Date Format
---------------
This is a UNIX-style globular matching pattern to describe how a date appears in each filename. You can use a series of literal characters combined with wildcards to tell Essentia how to extract the date from the filenames so it can obtain the date range over which your category takes place. This allows you to later take a subset of those files by specifying a custom date range that you want to pull data from. The key options you can provide it to symbolize each date/time segment are:

| **Y** = Year        
| **M** = Month       
| **D** = Day         
| **h** = Hour
| **m** = Minute
| **s** = Second

| By default Essentia tries to figure out the dates in your filenames using an **auto** setting. 
| For filenames that dont have dates in them you can also set the Date Format field to **none**.

**Example Date Format Patterns:** ::
    
    auto
    
    none
    
    *file_2014-06-09_out.zip:*

 	 \*Y-M-D\*
    
    *account12345678_20140609.csv:*

 	 *YMD.csv 
 	 
 	 Note: Here 'YMD' alone won't work since there is another 8 digit number, therefore we add the '.csv'. 
 	 In fact, just '.' would have been sufficient.
        
*Note:* For a more detailed description of globular matching patterns, see `Glob (programming) <http://en.wikipedia.org/wiki/Glob_%28programming%29>`_

Archive
---------------
This is a UNIX-style globular matching pattern to describe what types of files are included within your compressed files. You can use a series of literal characters combined with wildcards to tell Essentia which filenames within your compressed file belong in this category. This allows you to extract certain files from a compressed file archive while ignoring others.

**Example Archive Pattern:** ::
    
    Note: 'My_filename.zip' archive contains 'file_1_Site_12345' and 'file_1_Placement_12345'. 
    Match each of these files with the following Archive patterns:
    
    *Site*
    *Placement*
    
*Note:* For a more detailed description of globular matching patterns, see `Glob (programming) <http://en.wikipedia.org/wiki/Glob_%28programming%29>`_

Compression
---------------
A drop down to sleect the compression of the files in your category. Currently the options are **zip**, **gzip**, **tar**, and **none**.

Delimiter
---------------
The type of delimiter that your data uses. You can choose any single delimiter for your files. 

Selecting **NA** will cause Essentia not to attempt to determine your files' format. This allows you to select broad categories of files that may not be related or in a single format, or files that are in complicated formats either with many delimiters or no delimiter whatsoever. **NA** is a very useful option for simply exploring your datastore and discovering what files it contains.

Column Headers
---------------
These allow you to name your columns so you can reference them later. They **cannot contain spaces or special characters** and they **cannot start with a number**. These can be used in your sql statement in Direct Data Query to select and perform certain operations on specific columns in your data.

Data Types
---------------
The type of your data column. The options are **String**, **Unsigned Integer**, **Float**, **IP**, **X**, **C**, **Unsigned Long**, **Integer**, and **Long**. 

**X** is used to ignore an unwanted column and is highly recommended if you don't need a certain column or columns as it will speed up your queries even further.