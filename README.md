# language_resources
Code to construct language resources for a variety of languages 
##Setup
###Python
The code here has been was ran in `python 2.7.13` on Linux. Use of a tool such as [`pyenv`](https://github.com/yyuu/pyenv) (with [`virtualenv`](https://github.com/yyuu/pyenv-virtualenv)) to manage `python` versions is suggested. 

Required packages listed in `requirements.txt` can be installed through `pip` (`pip install -r requirements.txt`). Packages requiring a little more work are listed in `additional_requirements.txt`.

###brown-clustering 
To use the brown clustering script `cd` into `brown-clustering` and run `make`.

##Usage
###Brown clustering
`build_brown_clusters.py -i <input_file> -c <num_clusters> -o <output_directory>`
