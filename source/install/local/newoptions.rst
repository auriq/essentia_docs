******************************************
New Options for Local Essentia Version 3.1.0.3
******************************************

Essentia Version 3.1.0.3 contains some options that aren't mentioned anywhere else in the documentation. The two new options and the commands they affect are described below. 

There is also an additional command called ``udbsql`` which is described in :doc:`udbsql`.

Date Regex
---------------
This Date-regex option (``--dateregex``) can be used to match a regular expression 
pattern to the file paths and names in a category in order to extract the corresponding date. 
This increases the versatility of Essentia's date extraction by allowing 
regular expression patterns and will allow date extraction from much more 
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

| For filenames that dont have a date or number in them you can also set the Date Regex field to **none**.

.. %Y, %m, %d, %H, %M, %S, %p, %z -> [:%b:] - Jan, Feb, ..., Dec; [:%B:] - January, ..., December; "None" 
.. link to **regex** description and date format -> *Note:* For a more detailed description of globular matching patterns, see `Glob (programming) <http://en.wikipedia.org/wiki/Glob_%28programming%29>`_

File List Cache
---------------
This option (``--usecache``) stores a list of the files that are grouped into a category and references 
this list whenever that category is used. This list is static and must be updated 
if files in this category are changed or new files matching the file pattern are uploaded. 
This is a very useful feature for large repositories that have categories containing 
files spread across different directories or many undesired files in the same directory as the categorized files.

To change this option for a single category you would run ``ess category change name usecache [--usecache|--nocache]``.

Affected Commands:
-------------------------

.. csv-table::
    :header: "Command", "Arguments", "Description"
    :widths: 15, 25 ,30

    ess category add,"| name pattern 
    | ``[--dateregex regex_pattern|none]``
    | ``[--dateformat auto|none|custom]`` 
    | ``[--archive pattern]``
    | ``[--compression type|none]``
    | ``[--delimiter delimiter]``
    | ``[--columnspec NewColumnSpec]``
    | ``[--allx]``
    | ``[--alls]``
    | ``[--overwrite]``
    | ``[--label name]``
    | ``[--comment comment]``
    | ``[--noprobe]``
    | ``[--usecache]``","Add a category to the datastore"
    ess category change,"| columnspec|dateformat|dateregex|usecache|comment
    | NewSpec|NewFormat|NewRegex|NewCache|NewComment","Modify or override details about a category"    

The output of ``ess summary category`` is also affected and will display the original output plus the settings of these two new options (``--dateregex`` and ``--usecache``).
