.. **********************
.. **********************
===== 
データのリソースを定義する
===== 

Essentiaではまず、使用するデータのリソースを"datastore"として定義します。
現在Essentiaでサポートしているdatastoreタイプは下記です。

* ローカルディスクドライブ_
* AWSのS3データストア_
* Azureのblobストア_

AuriqではEssentiaを試用して頂くための サンプルデータ_ を公開しております。

------------

.. _ローカルディスクドライブ:

■ ローカルにあるファイルを使う場合 

  ::

    $ ess select local




.. _AWSのS3データストア:

■ AWSのS3バケットを使う場合

  ::

    $ ess select s3://bucket_name --credentials=~/your_credential_file.csv

  もしくは ::

    $ ess select s3://bucket_name --aws_access_key=XXX-YOURKEY-XXX --aws_secret_access_key=XXX-YOURSECRETKEY-XXX




.. _Azureのblobストア:

**■ AzureのBlobデータストアを使う場合** 

  パブリックコンテナの場合 ::

    $ ess select blob://private_container --account_name=associated_account --account_key=associated_key
  
  プライベートコンテナの場合 ::

    $ ess select blob://public_container --account_name=associated_account
  

------------


.. _サンプルデータ :

サンプルデータ
================

AuriqではチュートリアルやEssentiaのテストの為にサンプルデータを公開しております。

ローカルデータ
  `こちら <https://github.com/auriq/EssentiaPublic>`_ のgithubよりデータをpullしてご利用下さい。

AWS S3データ
  ::

    $ ess select s3://asi-public --credentials=~/mycredentials.csv

Azure Blob データ
  ::
    
    $ ess select blob://asi-public --account_name=asipublic




