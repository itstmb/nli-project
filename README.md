# Native Language Identification with User Generated Content

Extension: additional features and word embeddings

## Prerequisites

* Python Version 3.7.3+
* Disk Storage: 226 GB (OR UP TO 300GB with non_tokenized_chunks)

The following Python modules are a **must**:

* SciPy (and NumPy) <https://www.scipy.org/install.html>

* scikit-learn <https://scikit-learn.org/stable/install.html>

While it is possible to make your own data retrieval program, we highly recommend using the complete database:

<https://drive.google.com/drive/folders/125RAHvCIHBR-jAUnIhqzWhdxh0mQ_fcv>

(non_tokenized_chunks contains raw text and won't be used in our project)

In order to unzip the database, It is required to have 7zip: <https://www.7-zip.org/download.html>

**Please note**: You won't be able to generate your own vectors without the database, but you are still able to use the vectors we've made.

It is highly recommended to use PyCharm to view/edit the code. We have made a custom configuration file that highlights the important comments in different colors and makes it much easier to follow the algorithm process.

--------------------------------------------------------------------------------

## Installing

The database is very compressed, use 7zip in order to unzip the initial files, and then to unzip the outcome files again.

--------------------------------------------------------------------------------

## Config file

To apply the settings/config file, please follow the following steps:

1. Open PyCharm
2. File > Import Settings...
3. Select the settings.zip file under `./settings/settings.zip`
4. Make sure the Code Style (schemes) component is checked.
5. Press OK
6. Press OK again when prompted to restart PyCharm

You should now have the custom color schemes (highlighting) for the project:

Custom markdowns:

> OPTIMIZE - Parts of the code that we think could be optimized somehow (space/time).

> DEBUG - Parts of the code that are used in the debugging process.

> TEST - Parts of the code that still require some testing to make sure they do what we want them to.

> READY - This indicates that what is written after the tag should be working and ready to work with (helps with algorithm readability).

> MOTIVATION - Something that is yet to be implemented.

--------------------------------------------------------------------------------

## Running the code

There are multiple ways to run the project:

* Create the vectors yourself using the database / use the ready vectors
available on `./data`. This option saves alot of time if you intend to run the code on the database as is.
in order to create your own feature vectors, put in the database directory to generate vectors from.
```
python main.py 
```
or
```
python main.py /database_directory
```