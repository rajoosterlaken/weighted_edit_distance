# Weighted Edit Distance
Implementation for my thesis project on detecting valid name variant pairs using a weighted edit distance.

One of the requirements to boost the success of automated record linkage is to create a more reliable way to determine the validity of name variants as extracted from historical certificates.

The idea is that the cost method that usually drives edit distances can be dynamically influenced by earlier seen differences between names and use those to identify edit operations that are common between names.

For this purpose I created this very rough prototype of cost model training.
The resulting cost model could then be used to determine the costs of comparing name variants 


### Requirements
- **Python 3.6** or higher were used during development, running on earlier versions is not guaranteed to run.
- The `unidecode` Python package. While only used for the normalization of name variants this is required whether this is chosen to be done or not.


### Usage
To quickly run the program, follow these steps:



0. (Optional, but recommended) Create a virtual environment for the project:
   1. Make sure the [`virtualenv`](https://pypi.org/project/virtualenv/) package has been installed.
   2. Create a new environment in the cloned project's root directory:
   ```
   ...\weighted_edit_distance> virtualenv env
   ```
   3. Activate the environment:
   ```
   ...\weighted_edit_distance> env\Scripts\activate
   ```

1. Use `pip` to install the necessary packages as listed in `requirements.txt`:
```
(env) ...\weighted_edit_distance> pip3 install -r requirements.txt
```

2. Using `src` as the working directory, run the program:
```
(env) ...\weighted_edit_distance\src> python run_program.py
```

Applying these steps will run the program to create and collect 3 cost models based on the Dutch first name data (split in female/male) and surname data.

### Results
The output of the run described above will be generated in an `output` directory in the root directory of the project. The name of the subdirectory for the run will be the timestamp of when the run had been done (e.g. `"output\2018 08 13 15 32 42\"`).

In the run's directory, 3 `.pkl` files and 12 `.csv` files will have been generated:
- The `.pkl` files are pickled cost model objects, as described by the `src\cost_model.py` file.
- The `.csv` files are the results of analysing the data. This data was used as results in the thesis and mostly depicts the most likely substrings to be altered per name variant type per edit operation.

### Usage
This repository was mainly directed towards personal use. As such it contains elements that are unnecessary to apply the programming logic created for the cost model creation.

Looking at `cost_model.py` as a starting point might be the best choice to continue working with this program., mainly because `run_program.py` contains only logic used to create the test data found in the output directories after a run, which was useful for my thesis, but not for any future implementation.



### Other File Explanations:
Some files in this repository are not required to utilise the algorithm or its results.
This section highlights the files that could be disregarded.

- `latex.py` contains logic for converting a calculation table for a Levensthein edit distance algorithm into proper LaTeX syntax.


### Future Clean-up
Though it has fulfilled its purpose on my end, this code could use some refactoring/renaming and likely be optimised by including data processing packages such as `NumPy`, for which I simply did not feel the need.
