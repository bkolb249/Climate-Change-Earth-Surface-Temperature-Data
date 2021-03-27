# Climate-Change-Earth-Surface-Temperature-Data

# Structure of this Repo
I like to structure my code into a logic layer, that defines actual functions and classes, as well as the application layer, where the logic is applied and used. In this repository, the logic layer is given by the two files `eda.py` and `predictive_model.py`. The application layer is represented by the jupyter notebooks `01_EDA`, which makes use of the logic defined in `eda.py` to solve the problems of interest. Accordingly, the notebook `02_Predictive_Modelling` applies the modelling logic in `predictive_model.py`. The plots for EDA Task 1.3 can be found in the plots-folder. 

# Reproducing the Results
For reproducibility, the following is necessary:
- create a "data"-Folder in the root directory and place the unpacked data archive (including the "archive"-folder)
- install the requirements: `pip install -r requirements.txt`. This can be done in a Virtual environment (`python -m venv venv` -> `venv/Scripts/activate` and then the install command mentioned before) or in the jupyter notebook itself

# Comprehension of the Solution
It's probabily most easy to follow along the solution in the jupyter notebooks. There, all important conceptual information is given. More technical information can be found in the .py files. It is also possible to comprehend the solutions by viewing the html-versions of the notebokks in the folder html/. Then, the results can be viewed in the browser without needing to install anything. However, then the code can of course not be run.

# Model Details
I decided to model the temperatures in the cities with a simple Holt-Winters model. Details are documented in the Notebook `02_Predictive_Modelling`.

# General Statement to the Task
I actually needed the whole time for the task. I stuck a while on the approach for the modelling task, as the task was not 100% clear to me. I am sure that under normal working conditions some questions could have been clarified much faster. Also, I was not quite sure in what form you want the results. Jupyter notebook, both as `.ipynb` and as `.html` seemed to me to be the most practical solution. Hope its fine like that. Things that are currently still missing are especially input validation (and unit tests) for all functions / methods.