# Native Language Identification with User Generated Content

Extension: additional features and word embeddings

## Prerequisites

* Python Version 3.7.3+
* Disk Storage: 226 GB (OR UP TO 300GB with non_tokenized_chunks) (OR 1GB with the ready vector files)

The following Python modules are a **must**:

* SciPy (and NumPy) <https://www.scipy.org/install.html>

* scikit-learn <https://scikit-learn.org/stable/install.html>

While it is possible to make your own data retrieval program, we highly recommend using the complete database:

<https://drive.google.com/drive/folders/125RAHvCIHBR-jAUnIhqzWhdxh0mQ_fcv>

(non_tokenized_chunks contains raw text and which is unnecessary in our project)

To unzip the database, you are required to have 7zip: <https://www.7-zip.org/download.html>

**Please note**: You won't be able to generate the vectors without the database, but you are still able to use the vectors we have made. However some of the vector .txt files are too large to share on GitHub, thus you will be required to generate them yourself to classify using those features.

It is highly recommended to use PyCharm to view/edit the code. We have made a custom configuration file that highlights the essential comments in different colors and makes it much easier to follow the algorithm process.

--------------------------------------------------------------------------------

## Installing

The database is very compressed, use 7zip to unzip the original files, and then to unzip the outcome files again.

--------------------------------------------------------------------------------

## Running the code

There are multiple ways to run the project:

* Create the vectors yourself using the database / use the ready vectors. 
This option saves a lot of time if you intend to run the code on the database as is.
If you don't have any file that the algorithm requires in order to provide the vectors, it will generate the vector from the database specified in `database_dir.txt`.

```
python run.py
```

We've made a simple GUI interface for an intuitive user experience.

![GUI Interface](https://i.imgur.com/5nm64Gj.png)

Parameters:
Feature - The feature to use in the classification process.

Type - The type of classification (binary/language families/languages).

Domain - In domain trains and tests the classifier on the same data, out domain uses different data to test the classifier.

Threads - How many threads should be allocated for the classification process, depends on your hardware. -1 means utilize all threads.

Iterations - The limit of iterations for the classifier, a higher value will give more precise results.

--------------------------------------------------------------------------------

## Credits
Based on the paper "Native Language Identification with User Generated Content" (November 2018).  
Gili Goldin, Ella Rabinovich, Shuly Wintner.  
The paper is available online: https://aclweb.org/anthology/papers/D/D18/D18-1395/  
