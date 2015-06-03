**************************************
Getting Started with the Essentia UI
**************************************


*This guide will help walk you through the basic setup of the Essentia Data Viewer.*

Repository setup and management
--------------------------------

**Link to AWS S3**

1. Click on **Repository** in the sidebar and then the AWS S3 tab.
2. Click on the Add (+) icon to open the input form.
3. Enter your AWS S3 credentials (bucket name, access key, secret access key).
4. Click on the **Add** button to add your S3 repository.
5. Your newly added repository will be displayed in the AWS S3 table.

**Link to Azure Blob**

1. Click on **Repository** in the sidebar and then the Azure Blob tab.
2. Click on the Add (+) icon to open the input form.
3. Enter your Azure Blob credentials (container name, username, password).
4. Click on the **Add** button to add your Blob repository.
5. Your newly added repository will be displayed in the Azure Blob table.

**Delete Repository**

1. Click on **Repository** in the sidebar.
2. Choose the appropriate tab (AWS S3 or Azure Blob).
3. Select the delete (trash) icon for the repository you want to remove.
4. Confirm to delete your setting.

Datastore category setup and management
-----------------------------------------

**Create category**

1. Click on **Datastore** in the sidebar and select a Repository from the drop down.
2. Click on the Add (+) icon to open the input form.
3. Define your Category by entering:

* `Category name <http://www.auriq.com/documentation/source/reference/category-rules.html#category-name>`_ - any arbitrary name (no spaces)
* `Pattern <http://www.auriq.com/documentation/source/reference/category-rules.html#pattern>`_ - globular matching pattern to describe what types of files to include in your category
* `Comment <http://www.auriq.com/documentation/source/reference/category-rules.html#comment>`_ - any arbitrary comment

4. Define Category Options (optional) to speed up data scanning (see section 2 for more detail).
5. Click on the **Save** button to create your category. This may take a few minutes while Essentia scans your data.
6. After scan is complete, the derived column specifications will be displayed along with metadata about your files. Also, you can now choose to **Edit Columns** (see section 3 for more detail).
7. Your newly added category will be displayed in the category table for the selected repository. From here you can edit, copy or delete a category, view a sample of the data or see the list of files that make up your category.

**Define Category Options**

1. Follow steps 1-3 of creating a category.
2. Click on the options drop down arrow to display category options.
3. Define any or all of the following options:

* `Date Format <http://www.auriq.com/documentation/source/reference/category-rules.html#date-format>`_ - matching date format pattern found in filename structure
* `Archive <http://www.auriq.com/documentation/source/reference/category-rules.html#archive>`_ - matching pattern to describe filenames within a compressed file
* `Compression <http://www.auriq.com/documentation/source/reference/category-rules.html#compression>`_ - drop down to select the type of file compression
* `Delimiter <http://www.auriq.com/documentation/source/reference/category-rules.html#delimiter>`_ - the type of delimiter (comma, space, tab, etc) used in your data.

**Edit Columns**

1. Follow steps 1-5 of creating a category.
2. Click on the **Edit Columns** drop down arrow to view the current column spec details.
3. From here, you can change `column headers <http://www.auriq.com/documentation/source/reference/category-rules.html#column-headers>`_ (no spaces) and assign `data types <http://www.auriq.com/documentation/source/reference/category-rules.html#data-types>`_ in case the scan was not correct.
4. Click on the **Save** button to save your changes.

Query setup and management
-----------------------------

**Create a Query**

1. Click on **Direct Query** in the sidebar and and select a Repository from the drop down
2. Enter your SQL like query in the **Try New Query** input area.
3. Click on the **Run** button to view your query results on your screen or download it to file by entering a filename and clicking **Download**.
4. From this point you can save your query or run a new query.

*Note:* If you need to view available categories, click on the **Categories** drop down arrow to view a list of available categories.

`Query Format <http://www.auriq.com/documentation/source/reference/direct-query-examples.html>`_ ::

    select [column_name] | [*] from [category_name]:[start_date | *]:[end_date | *] where ... order by ... limit ...

    select count(distinct [column_name] | [*]) from [category_name]:[start_date | *]:[end_date | *]  where ...

    select [column_name], count(*) from from [category_name]:[start_date | *]:[end_date | *]  where ... group by [column_name]
    
`Example <http://www.auriq.com/documentation/source/reference/direct-query-examples.html>`_ ::

    select * from myfavoritedata:*:* where payment >= 50
    select * from purchase:2014-09-01:2014-09-15 where articleID>=46 limit 10
    
To see more examples of the queries we offer and work with some sample queries of our public data, please go through our :doc:`./direct-query-examples`