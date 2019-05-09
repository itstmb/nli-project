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

## Config file

To apply the tags(color patterns) configurations for better readability:

* Option 1 (APPEND):
1. Open PyCharm config options directory (usually `C:\Users\YOUR_USERNAME\.PyCharmCE2018.3\config\options`)
2. Use a text editor to open the `editor.xml` file
3. add the following pattern tags under the `TodoConfiguration` component (below the \bfixme\b.* pattern):

```
    <pattern useCustomColors="true" case-sensitive="true" pattern="\bOPTIMIZE\b.*">
      <option name="FOREGROUND" value="6e05f1" />
      <option name="FONT_TYPE" value="3" />
      <option name="ERROR_STRIPE_COLOR" value="7c27d7" />
    </pattern>
    <pattern useCustomColors="true" case-sensitive="true" pattern="\bDEBUG\b.*">
      <option name="FOREGROUND" value="cec27b" />
      <option name="FONT_TYPE" value="3" />
      <option name="ERROR_STRIPE_COLOR" value="e3e081" />
    </pattern>
    <pattern useCustomColors="true" case-sensitive="true" pattern="\bTEST\b.*">
      <option name="FOREGROUND" value="bf40" />
      <option name="BACKGROUND" value="ffb200" />
      <option name="FONT_TYPE" value="3" />
      <option name="ERROR_STRIPE_COLOR" value="61e367" />
    </pattern>
    <pattern useCustomColors="true" case-sensitive="true" pattern="\bREADY\b.*">
      <option name="FOREGROUND" value="fafffb" />
      <option name="BACKGROUND" value="b30f" />
      <option name="FONT_TYPE" value="3" />
      <option name="EFFECT_TYPE" value="5" />
    </pattern>
    <pattern useCustomColors="true" case-sensitive="true" pattern="\bMOTIVATION\b.*">
      <option name="FOREGROUND" value="fcfff9" />
      <option name="BACKGROUND" value="bf89" />
      <option name="FONT_TYPE" value="3" />
    </pattern>
```

4. Save
5. Restart Pycharm to apply those settings

* Option 2 (REPLACE):
Another way to apply those setting is to replace your `editor.xml` file with the one in the `project/settings` directory. Note that doing so will erase your other custom Editor configurations if you had any.

You should now have the custom color schemes (highlighting) for the project:

Custom markdowns:

> OPTIMIZE - Parts of the code that we think could be optimized somehow (space/time).

> DEBUG - Parts of the code that we use in the debugging process.

> TEST - Parts of the code that still require some testing to make sure they do what we want them to.

> READY - This indicates that what is mentioned after the tag should be working and ready to work with (helps with algorithm readability).

> MOTIVATION - Something we intend to implement in the future.

--------------------------------------------------------------------------------

## Running the code

There are multiple ways to run the project:

* Create the vectors yourself using the database / use the ready vectors
available on `./data`. This option saves a lot of time if you intend to run the code on the database as is.
To create the feature vectors, put in the database directory by the end of the command.
```
python main.py 
```
or
```
python main.py /database_directory
```

--------------------------------------------------------------------------------

## Credits
Based on the paper "Native Language Identification with User Generated Content" (November 2018).  
Gili Goldin, Ella Rabinovich, Shuly Wintner.  
The paper is available online: https://aclweb.org/anthology/papers/D/D18/D18-1395/  
