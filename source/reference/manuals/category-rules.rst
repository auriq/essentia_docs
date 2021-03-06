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

You can include multiple patterns separated by a space to group files that match multiple patterns into the same category. 

**Example of Multiple Patterns:** ::

    'diy_woodworking/*purchase* diy_woodworking/*browse*'
    # This will include ALL of the tutorial browse and purchase files.
    
    'filetypes/b.zip filetypes/"b test.zip"'
    # You can include a literal space in your pattern by quoting that pattern.

*Note:* For a more detailed description of globular matching patterns, see `Glob (programming) <http://en.wikipedia.org/wiki/Glob_%28programming%29>`_

*Note:* **Exclude** further restricts the files included by your **Pattern**.

Exclude
---------------
This is a UNIX-style globular matching pattern to describe what types of files to exclude from your category. You can use a series of literal characters combined with wildcards to tell Essentia that any filenames that match this pattern do **NOT** belong in this category. This is a sub-pattern that further restricts the files included by your **Pattern**.

*Note:* For a more detailed description of globular matching patterns, see `Glob (programming) <http://en.wikipedia.org/wiki/Glob_%28programming%29>`_

Comment
---------------
This field can contain any character and is just used to help you make notes about your categories or the files they contain.

Date Regex
---------------
This Date-regex option (``--dateregex``) can be used to match a regular expression 
pattern to the file paths and names in a category in order to extract the corresponding date. 
This enables Essentia's highly versatile date and number extraction by allowing 
regular expression patterns that can extract dates from incredibly 
complex or unique file paths and names.

The key options you can provide it to symbolize each date segment are:

| **Date and Time:**
| **[:%Y:]** = Four Digit Year 
| **[:%y:]** = Two Digit Year       
| **[:%m:]** = Two Digit Month
| **[:%b:]** = Three Letter Month (Jan, Feb, ..., Dec)
| **[:%B:]** = Text Month (January, ..., December)
| **[:%d:]** = Two Digit Day         
| **[:%H:]** = Two Digit Hour
| **[:%M:]** = Two Digit Minute
| **[:%S:]** = Two Digit Second
| **[:%z:]** = TimeZone
| **[:%p:]** = Case Insensitive AM or PM.

You can also provide the following option to extract just a number from the file path/name as a unique identifier:

| **Number:**
| **[:%f:{min,max}]** = Any Single Integer. Match from min to max digits. It is required to specify min; however, it is not necessary to specify max. If max is not specified, any number with at least min digits will be used as the unique identifier.

| By default Essentia tries to figure out the dates in your filenames using an **auto** setting. 
| You can also specify a custom **regex** pattern that identifies where the date or number appears in your file paths/names. 
| For file paths/names that don't have a date or number in them you can also set the Date Regex field to **none**. This will tell Essentia not to extract the date and will set the date field to a default, 1970-01-01.

.. note:: 
   If you don't specify Date Regex or Date Format (see below), then Essentia uses **auto** to extract the date from your filename. If no date can be extracted, Essentia reverts to the **none** behavior and defaults the date to 1970-01-01. 

**Example Date Format Patterns:** ::
    
    auto
    
    none
    
    .*file_2014-06-09_out.zip:.*

 	 .*[:%Y:]-[:%m:]-[:%d:].*
    
    .*account12345678_20140609.csv:.*

 	 .*[:%Y:][:%m:][:%d:].csv 
 	 
 	 Note: Here '[:%Y:][:%m:][:%d:]' alone won't work since there is another 8 digit number, therefore we add the '.csv'. 
  	 
    .*account12345678_20140609.csv:.*
    
         _[:%Y:][:%m:][:%d:]
         
         Note: This is another way to extract the date from this filename. Here we added '_' before the date 
         to help identify the date in the filename.
 	 
    .*account12345678_20140609.csv:.*
    
         [:%f:{8,}]_
         
         Note: This extracts the number from this filename. Here we added '_' after the number 
         to help identify the number in the filename.
         
    .*account12345678_20140609.csv:.*
    
         account[:%f:{8,}]
         
         Note: We could also have specified 'account' before the number to identify the number in the filename.
         
    .*account12345678_20140609.csv:.*
    
         account[:%f:{4,4}]
         
         Note: By specifying the min and max digits to 4, we use only the first four digits ('1234') as the identifying number in the filename.

*Note:* For a more detailed description of regex matching patterns, see `Regular Expression <https://en.wikipedia.org/wiki/Regular_expression>`_

Date Format
---------------

*Warning: Deprecated after Essentia version 3.1.0.7. Will be removed in the near future. Use Date Regex instead.*

This is a UNIX-style globular matching pattern to describe how a date or number appears in each filename. You can use a series of literal characters combined with wildcards to tell Essentia how to extract the date or number from the filenames so it can obtain the date range or number range over which your category takes place. This allows you to later take a subset of those files by specifying a custom date range or number range that you want to pull data from. The key options you can provide it to symbolize each date/number segment are:

| **Date and Time:**
| **Y** = Four Digit Year 
| **y** = Two Digit Year       
| **M** = Two Digit Month or Text Month (jan,January)       
| **D** = Two Digit Day         
| **h** = Two Digit Hour
| **m** = Two Digit Minute
| **s** = Two Digit Second
| **Z** = TimeZone
| **P** = Case Insensitive AM or PM.

| **Number:**
| **#** = Any Integer

| By default Essentia tries to figure out the dates in your filenames using an **auto** setting. 
| You can also specify a **custom** pattern that identifies where the date or number appears in your filenames. 
| For filenames that don't have a date or number in them you can also set the Date Format field to **none**.
        
**Example Date Format Patterns:** ::
    
    auto
    
    none
    
    *file_2014-06-09_out.zip:*

 	 *Y-M-D*
    
    *account12345678_20140609.csv:*

 	 *YMD.csv 
 	 
 	 Note: Here 'YMD' alone won't work since there is another 8 digit number, therefore we add the '.csv'. 
 	 In fact, just '.' would have been sufficient.
 	 
    *account12345678_20140609.csv:*
    
         _YMD
         
         Note: This is another way to extract the date from this filename. Here we added '_' before the date 
         to help identify the date in the filename.
 	 
    *account12345678_20140609.csv:*
    
         #_
         
         Note: This extracts the number from this filename. Here we added '_' after the number 
         to help identify the number in the filename.
         
    *account12345678_20140609.csv:*
    
         account#
         
         Note: We could also have specified 'account' before the number to identify the number in the filename.
        
*Note:* For a more detailed description of globular matching patterns, see `Glob (programming) <http://en.wikipedia.org/wiki/Glob_%28programming%29>`_

*Note:* It is recommended to use regular expression patterns to extract the date from your filename, see **Date Regex**.

.. %Y, %m, %d, %H, %M, %S, %p, %z -> [:%b:] - Jan, Feb, ..., Dec; [:%B:] - January, ..., December; "None" 
.. link to **regex** description and date format -> *Note:* For a more detailed description of globular matching patterns, see `Glob (programming) <http://en.wikipedia.org/wiki/Glob_%28programming%29>`_

Delimiter
---------------
The type of delimiter that your data uses. You can choose any single delimiter for your files. 

Selecting **noprobe** will cause Essentia not to attempt to determine your files' format. This allows you to select broad categories of files that may not be related or in a single format, or files that are in complicated formats either with many delimiters or no delimiter whatsoever. **noprobe** is a very useful option for simply exploring your datastore and discovering what files it contains.

Archive
---------------
This is a UNIX-style globular matching pattern to describe what types of files are included within your 
compressed or uncompressed archive files. You can use a series of literal characters combined with wildcards to tell Essentia which 
filenames within your compressed or uncompressed file belong in this category. This allows you to extract certain files from 
a compressed or uncompressed file archive while ignoring others.

**Example Archive Pattern:** ::
    
    Note: 'My_filename.zip' archive contains 'file_1_Site_12345' and 'file_1_Placement_12345'. 
    Match each of these files with the following Archive patterns:
    
    *Site*
    *Placement*
    
*Note:* For a more detailed description of globular matching patterns, see `Glob (programming) <http://en.wikipedia.org/wiki/Glob_%28programming%29>`_

Use Cached File List
--------------------
This option (``--usecache``) references a cached list of the files whenever the category is used. 
This bypasses Essentia's update process (where it looks at changes to the files on the repository that match the category's pattern(s)) and is meant to save time on large repositories.
Therefore, this option can cause your category to be out-of-date if files in this category are changed or new files matching the file pattern are uploaded on your repository. 
This is a very useful feature for large repositories that have categories containing 
files spread across different directories or many undesired files in the same directory as the categorized files.

.. note:: 

    Essentia's cached file list will still be updated anytime a category without the 
    ``--usecache`` option is used. This can cause your categories utilizing ``--usecache`` to have a different number of matching files than when you created the category, depending on what changes have been made to the repository.

To change this option for a single category you would run ``ess category change name usecache [--usecache|--nocache]``.

Preprocess
---------------
This option allows you to apply a command to the data in your category before Essentia tries to automatically detect its structure. This can be very helpful when your data contains many different delimiters or data that isn't simply delimited. You can view a sample of your raw data as well as enter a preprocessing command and check what the data will look like after that command is applied. Examples of where this is useful:

**Data With Multiple Delimiters:**

*Data*::

    54.248.98.72 - - [05/Oct/2014:03:24:27 -0700] "GET / HTTP/1.0" 301 - "-" "Mozilla/5.0 (compatible; monitis - premium monitoring service; http://www.monitis.com)"

*Preprocess Command*::

    aq_pp -f,eok,qui,div - -d ip:ip sep:" " s:rlog sep:" " s:rusr sep:" [" s:time_s sep:"] \"" s,clf:req_line1 sep:" " s,clf:req_line2 sep:" " s,clf:req_line3 sep:"\" " i:res_status sep:" " i:res_size sep:" \"" s,clf:referrer sep:"\" \"" s,clf:user_agent sep:"\"" -eval i:time "DateToTime(time_s, \"d.b.Y.H.M.S.z\")" -c ip rlog rusr time req_line1 req_line2 req_line3 res_status res_size referrer user_agent
    
*Sample Output*::

    54.248.98.72,"-","-",1412504667,"GET","/","HTTP/1.0",301,0,"-","Mozilla/5.0 (compatible; monitis - premium monitoring service; http://www.monitis.com)"

**Fixed Width Data:**
    
*Data*::

    STN--- WBAN   YEARMODA    TEMP       DEWP      SLP        STP       VISIB      WDSP     MXSPD   GUST    MAX     MIN   PRCP   SNDP   FRSHTT
    030050 99999  19320101    43.2  6    40.3  4   993.9  6  9999.9  0    4.3  6   10.2  6   18.1  999.9    45.0*   35.1   0.20F 999.9  010000

*Preprocess Command*::

    aq_pp -f,+1,eok,fix - -d s,n=7,trm:stn s,n=7,trm:wban s,n=12,trm:yearmoda s,n=6,trm:temp s,n=5,trm:unlabeled1 s,n=6,trm:dewp s,n=4,trm:unlabeled2 s,n=7,trm:slp s,n=3,trm:unlabeled3 s,n=1,trm:unlabeled4 s,n=7,trm:stp s,n=3,trm:unlabeled5 s,n=7,trm:visib s,n=4,trm:unlabeled6 s,n=6,trm:wdsp s,n=3,trm:unlabeled7 s,n=7,trm:mxspd s,n=1,trm:unlabeled8 s,n=8,trm:gust s,n=8,trm:max s,n=6,trm:min s,n=7,trm:prcp s,n=7,trm:sndp s,n=6,trm:frshtt
..    logcnv -f,+1,eok - -d s,n=7:stn s,n=7:wban s,n=12:yearmoda s,n=6:temp s,n=5:unlabeled1 s,n=6:dewp s,n=4:unlabeled2 s,n=7:slp s,n=3:unlabeled3 s,n=1:unlabeled4 s,n=7:stp s,n=3:unlabeled5 s,n=7:visib s,n=4:unlabeled6 s,n=6:wdsp s,n=3:unlabeled7 s,n=7:mxspd s,n=1:unlabeled8 s,n=8:gust s,n=8:max s,n=6:min s,n=7:prcp s,n=7:sndp s,n=6:frshtt
    
*Sample Output*::

    "stn","wban","yearmoda","temp","unlabeled1","dewp","unlabeled2","slp","unlabeled3","unlabeled4","stp","unlabeled5","visib","unlabeled6","wdsp","unlabeled7","mxspd","unlabeled8","gust","max","min","prcp","sndp","frshtt"
    "030050","99999","19320101","43.2","6","40.3","4","993.9","6","9","999.9","0","4.3","6","10.2","6","18.1","9","99.9","45.0*","35.1","0.20F","999.9","010000"

**Json Data:** 
    
*Data*::

    {
    "coordinates": null,
    "created_at": "Thu Oct 21 16:02:46 +0000 2010",
    "favorited": false,
    "truncated": false,
    "id_str": "28039652140",
    "entities": {
        "urls": [
        {
            "expanded_url": null,
            "url": "http://gnip.com/success_stories",
            "indices": [
            69,
            100
            ]
        }
        ],
    ...
    },
    "in_reply_to_user_id_str": null,
    "text": "what we've been up to at @gnip -- delivering data to happy customers http://gnip.com/success_stories",
    ...
    "user": {
        "profile_sidebar_border_color": "C0DEED",
        "name": "Gnip, Inc.",
    ...
    },
    "in_reply_to_screen_name": null,
    "source": "web",
    "place": null,
    "in_reply_to_status_id": null
    }

*Preprocess Command*::

    aq_pp -f,eok,jsn twitterex.json -d s:coordinates:coordinates s:created_at:created_at s:favorited:favorited s:truncated:truncated s:id_str:id_str s:in_reply_to_user_id_str:in_reply_to_user_id_str s:text:text s:profile_sidebar_border_color:user.profile_sidebar_border_color s:name:user.name s:in_reply_to_screen_name:in_reply_to_screen_name s:source:source s:place:place s:in_reply_to_status_id:in_reply_to_status_id
    
*Sample Output*::

    "coordinates","created_at","favorited","truncated","id_str","expanded_url","url","in_reply_to_user_id_str","text","profile_sidebar_border_color","name","in_reply_to_screen_name","source","place","in_reply_to_status_id"
    ,"Thu Oct 21 16:02:46 +0000 2010","false","false","28039652140",,"what we've been up to at @gnip -- delivering data to happy customers http://gnip.com/success_stories","C0DEED","Gnip, Inc.",,"web",,
    
.. Compression
.. ---------------
.. A drop down to sleect the compression of the files in your category. Currently the options are **zip**, **gzip**, **tar**, and **none**.
.. 

Column Headers
---------------
These allow you to name your columns so you can reference them later. They **cannot contain spaces or special characters** and they **cannot start with a number**. These can be used in your sql statement in Query to select and perform certain operations on specific columns in your data.

Data Types
---------------
The type of your data column. The options are **String**, **Unsigned Integer**, **Float**, **IP**, **X**, **Unsigned Long**, **Integer**, and **Long**. 

**X** is used to ignore an unwanted column and is highly recommended if you don't need a certain column or columns as it will speed up your queries even further.

