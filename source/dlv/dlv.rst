***************
Getting Started
***************


*This guide will help walk you through the basic setup and use of the Essentia Data Lake Manager.*

To learn more about how to create a category, see :doc:`../reference/manuals/category-rules`.

Repository setup and management
--------------------------------

.. `Video Demo <https://www.youtube.com/watch?v=G5x4dDazFug&width=640&height=480>`_

.. `Video Demo <https://youtu.be/Bsoa7psCFgo>`_

**Link to AWS S3**

1. Click on **Connect** in the top menu and then the AWS S3 tab.
2. Click on the **+Add** icon to open the input form.
3. Enter your AWS S3 credentials (bucket name, access key, secret access key) and a label if you prefer to call the bucket by another name.
4. Click on the **Add** button to add your S3 repository.
5. Your newly added repository will be displayed in the AWS S3 table.

.. image:: ../screenshots/connect_aws_add.png
   :align: center
   :scale: 30
   :target: ../screenshots/connect_aws_add.png


**Link to Azure Blob**

1. Click on **Connect** in the top menu and then the Azure Blob tab.
2. Click on the **+Add** icon to open the input form.
3. Enter your Azure Blob credentials (container name, username, password) and a label if you prefer to call the container by another name.
4. Click on the **Add** button to add your Blob repository.
5. Your newly added repository will be displayed in the Azure Blob table.

.. image:: ../screenshots/connect_azure_add.png
   :align: center
   :scale: 30
   :target: ../screenshots/connect_azure_add.png

**Delete Repository**

1. Click on **Connect** in the top menu.
2. Choose the appropriate tab (AWS S3 or Azure Blob).
3. Click the icon on the right of the table for the repository you want to remove.
4. Select the delete (trash) icon.
5. Confirm to delete your setting.

.. image:: ../screenshots/connect_delete.png
   :align: center
   :scale: 30
   :target: ../screenshots/connect_delete.png
   
Datastore category setup and management
---------------------------------------

.. `Video Demo <https://youtu.be/ed0g7uVzEmA>`_

**Create category**

1. Click on **Categorize** in the top menu and select a Repository from the drop down.
2. Click on the **+Add** icon to open the input form.
3. Define your Category by entering:

* `Category name <../reference/manuals/category-rules.html#category-name>`_ - any arbitrary name (no spaces).
* `Pattern <../reference/manuals/category-rules.html#pattern>`_ - globular matching pattern(s) to describe what types of files to include in your category.

4. Optionally define any number of the following options to speed up data scanning or make data management easier:

* `Comment <../reference/manuals/category-rules.html#comment>`_ - any arbitrary comment.
* `Delimiter <../reference/manuals/category-rules.html#delimiter>`_ - the type of delimiter (comma, space, tab, etc) used in your data.
* `Exclude <../reference/manuals/category-rules.html#exclude>`_ - globular matching pattern to describe what files to not include in your category. **Note:** this further restricts the files included by your ``Pattern``.
* `Date Format <../reference/manuals/category-rules.html#date-regex>`_ - matching date extraction pattern found in filename structure. Specify a regular expression pattern to extract the date from your file path/name, see `Date Regex <../reference/manuals/category-rules.html#date-regex>`_.

.. image:: ../screenshots/categorize_options.png
   :align: center
   :scale: 30
   :target: ../screenshots/categorize_options.png
   
5. Click on the **Save** button to create your category. This may take a few minutes while Essentia scans your data.
6. After scan is complete, the derived column specifications will be displayed along with metadata about your files. Also, you can now **Define Additional Category Options** (see section 2 for more detail) or choose to **Directly Edit Column Specification** (see section 3 for more detail).
7. Your newly added category will be displayed in the category table for the selected repository. From here you can edit, copy, scan, or delete a category, view a sample of the data or see the list of files that make up your category.

**Define Additional Category Options**

1. Follow steps 1-5 of creating a category.
2. Click on the preprocess drop down to **Check** or save a command to preprocess your data:

* `Preprocess <../reference/manuals/category-rules.html#preprocess>`_ - command to modify your raw data before it is scanned by Essentia.

3. Or click on the options drop down arrow to display category options and define either of the following options:

* `Archive <../reference/manuals/category-rules.html#archive>`_ - matching pattern to describe filenames within a compressed file.
* `Use cached file list <../reference/manuals/category-rules.html#use-cached-file-list>`_ - reference the local file list for the current category instead of accessing the repository.

.. * `Compression <../reference/manuals/category-rules.html#compression>`_ - drop down to select the type of file compression

**Directly Edit Column Specification**

1. Follow steps 1-5 of creating a category.
2. Click on the **Direct Edit** checkbox to allow the current column spec to be edited.
3. From here, you can change `column headers <../reference/manuals/category-rules.html#column-headers>`_ (no spaces) and assign `data types <../reference/manuals/category-rules.html#data-types>`_ in case the scan was not correct.
4. Click on the **Save** button to save your changes.

**Exploring Your Data Repository**

1. Click **Explore**.
2. Click the **+** next to a directory to navigate through the directories on your Repository.
3. Your current path is displayed at the top, under your repository name. This is useful when defining a pattern for the files you want to group into a category.
4. You can click the icon next to any filename to **Download** or **Delete** that file from your Repository.

.. image:: ../screenshots/categorize_explore_dwnld.png
   :align: center
   :scale: 30
   :target: ../screenshots/categorize_explore_dwnld.png
   
You can click **Upload** to choose files to upload to the current path on your Repository.

You can click **Size** to calculate the total number of files and bytes in the current path on your Repository.

You can click **Refresh** to get the latest list of files on your Repository.

*Note:* If the Explorer tab does not open when you click **Explore**, you may need to enable pop-ups from the Essentia UI.

Query setup and management
-----------------------------

.. `Video Demo <https://youtu.be/jILkSbnPHeg>`_

**Create a Query**

1. Click on **Query** in the top menu and and select a Repository from the drop down
2. Enter your SQL like query in the **Input your query here** area. You can optionally enter a label for this query so you can reference it later. 
3. Click on the **Run** button to view your query results on your screen and then optionally download your query results into a file on your computer by clicking **Download** and entering a filename.
4. If you do not need the results of your query anymore, you can click **Clear** to delete those results. 
5. From this point you can access a saved query or run a new query. Running another query will clear the previous query's results.

.. image:: ../screenshots/query_run.png
   :align: center
   :scale: 30
   :target: ../screenshots/query_run.png
   
.. , or generate an OData link for easy loading into Tableau by clicking **OData**.

| 
*Note:* If you need to view available categories, click on the **Categories** drop down arrow to view a list of available categories.

.. image:: ../screenshots/query_categories.png
   :align: center
   :scale: 30
   :target: ../screenshots/query_categories.png
   
`Query Format <../dlv/direct-query-examples.html>`_ ::

    select [column_name] | [*] from [category_name]:[start_date | *]:[end_date | *] where ... order by ... limit ...

    select count(distinct [column_name] | [*]) from [category_name]:[start_date | *]:[end_date | *]  where ...

    select [column_name], count(*) from [category_name]:[start_date | *]:[end_date | *]  where ... group by [column_name]
    
`Rules <../dlv/direct-query-examples.html>`_ ::

    The first query format above is a "select" query.
    The second and third query formats above are "count" queries.
    
    1. Group By is NOT supported for SELECT queries. 
    2. Order By is NOT supported for COUNT queries.
    3. Limit is NOT supported for COUNT queries.
    4. Group By can only be used when there is no DISTINCT in COUNT queries.
    
`Example <../dlv/direct-query-examples.html>`_ ::

    select * from myfavoritedata:*:* where payment >= 50
    select * from purchase:2014-09-01:2014-09-15 where articleID>=46 limit 10
    
To see more examples of the types of queries we allow and work with some sample queries of our public data, please go through our :doc:`./direct-query-examples`

.. **Transfer Data with Tableau OData**
.. 
.. 1. Create a query following the steps above and click the **OData** button to generate an OData link to your query.
.. 2. Copy this Link using the **Copy** option on the right of the URL box or highlight the URL and copy it to your clipboard.
.. 3. Open Tableau and go to the "To a server" connection section.
.. 4. Select **OData**. Note, you need to click "More Servers" to see the OData option if you are using Tableau Desktop.
.. 5. Paste the URL into the box after "Server:" and select **No Authentication** (this should be the default).
.. 
.. | *Note:* 
.. |   Our OData service is still in its Beta version and is currently limited to sending 10,000 lines of data (and 100,000 values) *into* Tableau. However, you can *query* larger amounts of data as long as the *output* is less than 10,000 lines (and 100,000 values). This will be improved in the full version, which will be released in the near future, along with support for OData clients other than Tableau.

**Working with Saved Queries**

1. Select your Saved Query from the dropdown. The query should appear in the "Input your query here" area. If you labeled your query, the label should appear next to the saved query dropdown.
2. Now you can click the **Run** button to view your query results on your screen and then optionally download your query results into a file on your computer by clicking **Download** and entering a filename.

.. 2. Now you can click the **Run** button to view your query results on your screen, download your query results into a file on your instance by clicking **Download** and entering a filename, access the query via an http link by clicking **HTTP**, or generate an OData link for easy loading into Tableau by clicking **OData**.
.. You can generate a new HTTP link for your query by clicking **HTTP** and then clicking **Reset**. This is useful if you want to share the link with others, but only want to provide them access for a limited amount of time. 

You can search your saved queries by entering any parts of your desired queries into the **Search** box. 

Script setup and management
-----------------------------

.. `Video Demo <https://youtu.be/jILkSbnPHeg>`_

**Run a Script**

1. Click on **Analyze** in the top menu.
2. Select a Github Repository from the drop down menu or use the Default (DirectScipt - auriq).
3. Enter your Essentia or unix shell commands in the **Input your script here** area. You can optionally select one of the files from your Github Repository to edit or run. To do this, click the file icon to the left of the filename. 
4. Click on the **Run** button to view your script's results on your screen.

.. image:: ../screenshots/analyze_script.png
   :align: center
   :scale: 30
   :target: ../screenshots/analyze_script.png
   
*Note:* You can also **Stop** running your script or, when it has finished, **Download** the result onto your local machine or **Clear** the results so they are no longer stored.

.. image:: ../screenshots/analyze_script_run.png
   :align: center
   :scale: 30
   :target: ../screenshots/analyze_script_run.png
   
*Note:* You can also view the status of your master computer and any other machines you are utilizing by clicking on **Cluster Status**. This will show you the connection information and resource usage of each connected machine.

**Connect to a Github Repository**

1. Click on **Analyze** in the top menu.
2. Click the **Add** button.
3. Enter the **Owner** of your Github Repository, the name of your **Repository**, and your Personal Access **Token**. If you do not have a Personal Access Token, follow the instructions found `here <https://help.github.com/articles/creating-an-access-token-for-command-line-use/>`_.
4. Click on the **Save** button to finish adding your Github Repository.
5. From this point you can view, edit, and run any of the scripts stored in the Github Repository. 

.. To commit any changes back to you Github Repository, the Personal Access Token you used to connect to the repository must have had write permissions. If this is the case, you can click **Commit** to push your changes back onto the Github Repository.

*Note:* To view or switch between available Github Repositories or Branches, click on the **Github Repository** or **Branch** drop down menus.

Questions
---------

Our tutorials are intended to guide you through the usage of the included tools, but you should feel free to contact us at essentia@auriq.com with any other questions.