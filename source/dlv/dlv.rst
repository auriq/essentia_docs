***************
Getting Started
***************


*This guide will help walk you through the basic setup and use of the Essentia Data Lake Manager.*

Repository setup and management
--------------------------------

.. `Video Demo <https://www.youtube.com/watch?v=G5x4dDazFug&width=640&height=480>`_

`Video Demo <https://youtu.be/Bsoa7psCFgo>`_

**Link to AWS S3**

1. Click on **Data Repository** in the top menu and then the AWS S3 tab.
2. Click on the **+Add** icon to open the input form.
3. Enter your AWS S3 credentials (bucket name, access key, secret access key) and a label if you prefer to call the bucket by another name.
4. Click on the **Add** button to add your S3 repository.
5. Your newly added repository will be displayed in the AWS S3 table.

**Link to Azure Blob**

1. Click on **Data Repository** in the top menu and then the Azure Blob tab.
2. Click on the **+Add** icon to open the input form.
3. Enter your Azure Blob credentials (container name, username, password) and a label if you prefer to call the container by another name.
4. Click on the **Add** button to add your Blob repository.
5. Your newly added repository will be displayed in the Azure Blob table.

**Delete Repository**

1. Click on **Data Repository** in the top menu.
2. Choose the appropriate tab (AWS S3 or Azure Blob).
3. Click the icon on the right of the table for the repository you want to remove.
4. Select the delete (trash) icon.
5. Confirm to delete your setting.

Datastore category setup and management
---------------------------------------

`Video Demo <https://youtu.be/ed0g7uVzEmA>`_

**Create category**

1. Click on **Data Viewer** in the top menu and select a Repository from the drop down.
2. Click on the **+Add** icon to open the input form.
3. Define your Category by entering:

* `Category name <http://www.auriq.com/documentation/source/reference/manuals/category-rules.html#category-name>`_ - any arbitrary name (no spaces)
* `Pattern <http://www.auriq.com/documentation/source/reference/manuals/category-rules.html#pattern>`_ - globular matching pattern to describe what types of files to include in your category
* `Comment <http://www.auriq.com/documentation/source/reference/manuals/category-rules.html#comment>`_ - any arbitrary comment

4. Define Category Options (optional) to speed up data scanning (see section 2 for more detail).
5. Click on the **Save** button to create your category. This may take a few minutes while Essentia scans your data.
6. After scan is complete, the derived column specifications will be displayed along with metadata about your files. Also, you can now choose **Direct Edit** to edit the column specification (see section 3 for more detail).
7. Your newly added category will be displayed in the category table for the selected repository. From here you can edit, copy or delete a category, view a sample of the data or see the list of files that make up your category.

**Define Category Options**

1. Follow steps 1-3 of creating a category.
2. Define either or both of the following options:

* `Date Format <http://www.auriq.com/documentation/source/reference/manuals/category-rules.html#date-format>`_ - matching date format pattern found in filename structure
* `Delimiter <http://www.auriq.com/documentation/source/reference/manuals/category-rules.html#delimiter>`_ - the type of delimiter (comma, space, tab, etc) used in your data.

3. Or click on the options drop down arrow to display category options and define either of the following options:

* `Archive <http://www.auriq.com/documentation/source/reference/manuals/category-rules.html#archive>`_ - matching pattern to describe filenames within a compressed file
* `Preprocess <http://www.auriq.com/documentation/source/reference/manuals/category-rules.html#preprocess>`_ - command to modify your raw data before it is scanned by Essentia.
.. * `Compression <http://www.auriq.com/documentation/source/reference/manuals/category-rules.html#compression>`_ - drop down to select the type of file compression

**Directly Edit Column Specification**

1. Follow steps 1-5 of creating a category.
2. Click on the **Direct Edit** checkbox to allow the current column spec to be edited.
3. From here, you can change `column headers <http://www.auriq.com/documentation/source/reference/manuals/category-rules.html#column-headers>`_ (no spaces) and assign `data types <http://www.auriq.com/documentation/source/reference/manuals/category-rules.html#data-types>`_ in case the scan was not correct.
4. Click on the **Save** button to save your changes.

**Exploring Your Data Repository**

1. Click **Explore**.
2. Click the **+** next to a directory to navigate through the directories on your Repository.
3. Your current path is displayed at the top, next to your repository name. This is useful when defining a pattern for the files you want to group into a category.

You can click **Size** to calculate the total number of files and bytes in your Repository.

You can click **Refresh** to get the latest list of files on your Repository. 

Query setup and management
-----------------------------

`Video Demo <https://youtu.be/jILkSbnPHeg>`_

**Create a Query**

1. Click on **Direct Data Query** in the top menu and and select a Repository from the drop down
2. Enter your SQL like query in the **Input your query here** area. You can optionally enter a label for this query so you can reference it later. 
3. Click on the **Run** button to view your query results on your screen, download your query results into a file on your instance by clicking **Download** and entering a filename, or generate an OData link for easy loading into Tableau by clicking **OData**.
4. From this point you can access a saved query or run a new query.

*Note:* If you need to view available categories, click on the **Categories** drop down arrow to view a list of available categories.

`Query Format <http://www.auriq.com/documentation/source/dlv/direct-query-examples.html>`_ ::

    select [column_name] | [*] from [category_name]:[start_date | *]:[end_date | *] where ... order by ... limit ...

    select count(distinct [column_name] | [*]) from [category_name]:[start_date | *]:[end_date | *]  where ...

    select [column_name], count(*) from from [category_name]:[start_date | *]:[end_date | *]  where ... group by [column_name]
    
`Rules <http://www.auriq.com/documentation/source/dlv/direct-query-examples.html>`_ ::

    The first query format above is a "select" query.
    The second and third query formats above are "count" queries.
    
    1. Group By is NOT supported for SELECT queries. 
    2. Order By is NOT supported for COUNT queries.
    3. Limit is NOT supported for COUNT queries.
    4. Group By can only be used when there is no DISTINCT in COUNT queries.
    
`Example <http://www.auriq.com/documentation/source/dlv/direct-query-examples.html>`_ ::

    select * from myfavoritedata:*:* where payment >= 50
    select * from purchase:2014-09-01:2014-09-15 where articleID>=46 limit 10
    
To see more examples of the types of queries we allow and work with some sample queries of our public data, please go through our :doc:`./direct-query-examples`

**Transfer Data with OData**

1. Create a query following the steps above and click the **OData** button to generate an OData link to your query.
2. Copy this Link using the **Copy** option on the right of the URL box or highlight the URL and copy it to your clipboard.
3. Open Tableau and go to the "To a server" connection section.
4. Select **OData**. Note, you need to click "More Servers" to see the OData option if you are using Tableau Desktop.
5. Paste the URL into the box after "Server:" and select **No Authentication** (this should be the default).

| *Note:* 
|   Our OData service is still in its Beta version and is currently limited to sending 10,000 lines of data (and 100,000 values) *into* Tableau. However, you can *query* larger amounts of data as long as the *output* is less than 10,000 lines (and 100,000 values). This will be improved in the full version, which will be released in the near future, along with support for OData clients other than Tableau.

**Working with Saved Queries**

1. Select your Saved Query from the dropdown. The query should appear in the "Input your query here" area. If you labeled your query, the label should appear next to the saved query dropdown.
2. Now you can click the **Run** button to view your query results on your screen, download your query results into a file on your instance by clicking **Download** and entering a filename, access the query via an http link by clicking **HTTP**, or generate an OData link for easy loading into Tableau by clicking **OData**.

You can generate a new HTTP link for your query by clicking **HTTP** and then clicking **Reset**. This is useful if you want to share the link with others, but only want to provide them access for a limited amount of time. 

You can search your saved queries by entering any parts of your desired queries into the **Search** box. 

Using RStudio
-------------

**Setting up RStudio**

If you plan to use our RStudio Integration and you haven't enabled it yet, you need to:

1. Go to the AWS Console.
2. Right Click on your Instance, click **Instance State**, and **Stop** your instance.
3. Right Click on your Instance, click **Instance Settings**, and click **View/Change User Data**
4. Enter **"rstudio"**.
5. Right Click on your Instance, click **Instance State**, and **Start** your instance.

**Accessing RStudio**

Go to the UI and then click the **RStudio** link in the top menu. 

Enter **"essentia"** as the username and enter the **Instance ID** of your instance as your password.

You can now use all the capabilities of RStudio directly from your browser. 

**Running Essentia via RStudio**

Essentia's R Integration package is installed by default. To access it, you simply need to enter the R command **library(RESS)**. See our `R Integration Tutorial <http://www.auriq.com/documentation/source/integrations/R/index.html>`_ to see how to use the RESS package to integrate R and Essentia.

To run an Essentia Bash Script that already exists on your file system, you can simply run it from within RStudio by navigating to the directory that contains your script and entering **system("sh Your_Script_name.sh")**.

To create an Essentia Bash Script from within RStudio:

* Click **File** → **New File** → **Text File**
* Click **File** → **Save As**
* Enter your desired filename followed by **.sh** (Ex: Your_Script_Name.sh)

You are now free to enter any Essentia commands to accomplish your data preparation, integration, or analysis.

To Save your script, use a shortcut or click **File** → **Save**.

To run your script, navigate to the directory that contains your script and then either run **system("sh Your_Script_name.sh")** or click on **Run Script** in the top right of the Script Panel.

Questions
---------

Our tutorials are intended to guide you through the usage of the included tools, but you should feel free to contact us at info@auriq.com with any other questions.