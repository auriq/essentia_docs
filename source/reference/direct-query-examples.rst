******************************
Direct Data Query Examples
******************************

.. Example Direct Data Query Commands

.. **Required First Step**

.. Select your repository from the drop down menu. If you haven't defined a repository yet, click on the 'Data Repository' tab and add the repository that contains the data you want to explore.

**Overview**

Direct Data Query is Essentia's unique method of quering the data in your datastore directly, without loading anything into memory. 
It allows you to quickly and efficiently explore data in a multitude of formats and is written in a user friendly, SQL-like language.

The Direct Data Query command structure consists of a select statement to defined which columns are desired and what operations you want to perform on them, 
a from statement telling Direct Data Query which category in your repository to pull the data from and over what time period, and a series of filtering and ordering options to modify how the data is output.

This tutorial will provide sample usage of the currently supported options for Direct Data Query. These options are:

* **Select Statement Specifications:** *column_name(s), \*, count(column_name), count(\*), count(distinct column_name)*
* **From Statement Specifications:** *category_name:start_date:end_date*
* **Output Modification Options:** *where column_name operator value, limit number, group by column_name, order by column_name*

**Data Overview**

This tutorial works on the browse data on our *public* cloud storage, **asi-public**. To access this data:

First go to the **Data Repository** tab.


S3 users then go to the **AWS S3** panel and click the plus button. Enter::
    
    asi-public
    Your_Access_Key
    Your_Secret_Access_Key
    
and click **Add**. 

Azure users instead go to the **Azure Blob** panel and click the plus button. Enter::

    asi-public
    asipublic
    
    
and click **Add**. 

*Note*: The **Password** field is left empty since this is a *public* bucket.



Next go to the **Data Viewer** tab and select **asi-public** from the drop down menu.

Now click the plus button, enter ``browse`` next to **Category**, and the globular pattern ``diy_woodworking/*browse*`` under **Pattern**. 
Click **Save**. This finds all the files in our repository asi-public whose filenames match our pattern. 
It also displays the type and name of each column in the matching files. These columns are::

    S:eventDate I:userID I:articleID

Now that you have selected your datastore and defined a category, you can click **Direct Data Query** to start exploring your data.

*The rest of this tutorial highlights various commands you can enter into Direct Data Query. 
This is not a complete list but provides the building blocks from which you can build more complex queries. 
We also show the first five lines of the output of each command.*

**Sample Statement Usage**

Ouput every row of the userID column from files in the browse category between 2014-09-01 and 2014-09-02.

``select userID from browse:2014-09-01:2014-09-02`` ::

    75
    29
    30
    46
    76

Output every row of all columns from files in the browse category between 2014-09-01 and 2014-09-15.

``select * from browse:2014-09-01:2014-09-15`` ::

    "2014-09-01 00:03:28",75,213
    "2014-09-01 00:09:00",29,343
    "2014-09-01 00:11:02",30,485
    "2014-09-01 00:11:14",46,275
    "2014-09-01 00:14:23",76,241

Count the number of rows in the userID column from files in the browse category between 2014-09-10 and the end of the category's date range (2014-09-30 for the browse category).

``select count(userID) from browse:2014-09-10:*`` ::

    "row"
    13880

Count the number of rows from files in the browse category between the start of the category's date range (2014-09-01 in this case) and 2014-09-13. 
There is no difference between counting a single column and counting \* since they both measure the total number of rows.

``select count(*) from browse:*:2014-09-13`` ::

    "row"
    8786

Count the total number of unique values in the userID column from files in the browse category over the entire date range. The output is two columns: the number of rows in the data and the number of unique values in the userID column.

``select count(distinct userID) from browse:*:*`` ::

    "row","k_userID"
    19356,100
    
**Sample Output Modification Usage**

Only output the rows from the files in the browse category between 2014-09-01 and 2014-09-15 when they pass the condition that the value in the userID column is greater than or equal to 50.

``select * from browse:2014-09-01:2014-09-15 where userID >= 50`` ::

    "2014-09-01 00:03:28",75,213
    "2014-09-01 00:14:23",76,241
    "2014-09-01 00:21:01",92,259
    "2014-09-01 00:33:33",94,129
    "2014-09-01 00:35:44",80,120

Only output the first three rows from the files in the browse category between 2014-09-01 and 2014-09-15.

``select * from browse:2014-09-01:2014-09-15 limit 3`` ::

    "2014-09-01 00:03:28",75,213
    "2014-09-01 00:09:00",29,343
    "2014-09-01 00:11:02",30,485

Output the number of times a unique value of the userID was observed in the files from the browse category over the entire date range.

``select count(distinct userID) from browse:*:* group by userID`` ::

    "userID","Count"
    6,202
    7,187
    8,202
    9,219
    
Output all of the rows from files in the browse category over the entire date range, ordered by the values in the articleID column in ascending order.
    
``select * from browse:*:* order by articleID`` ::

    "2014-09-01 10:07:23",96,1
    "2014-09-02 07:14:01",17,1
    "2014-09-02 21:33:00",57,1
    "2014-09-03 21:44:22",43,1
    "2014-09-05 03:39:12",47,1