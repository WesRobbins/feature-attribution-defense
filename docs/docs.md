# docs
- github repo for code instead of shared drive folder
- still save trained models in shared folder
- save experimentation figures in shared folder

### database.py
functions for accessing nosql database for result
- write_databse : writes expiement result to database
- read_database : query databse for results

### visualizations.py
visualization of images 
- show_images : show images from dataset 
    - params: dataset, labels(t/f), num_images 
    - option for showing classification from given model
        - maybe even classifications from several models
- show_features : show feature attribution
    - options: also show normal images,  which attribution method, dataset
    - option to compare clean image attribution to adversarial image attribution
- attribution_hist : histogram of feature attributions
    - option to overlay several several attributions on same histogram (like ML-LOO paper)

### results-grahps.py
create graphs/visualization from results of attacks vs defenses

### attribution-alalysis.py 
numerical analsys on attribution to allow for comparisons between adversarial attributions vs clean attributions. all functions passed in an attribution tensor
- std_deviation
- mean 
- some anomaly detection methods
- find others later

### result.py
file has a 'result' class. all experiment functions should return objects of this class. Will be helpful if we want to keep track of things instead of just accuracy at some point. I think it will be easier than just returning lists/dictionaries.

**class result**
attributes
- identifier
- attack
- attack_strength
- defense
- model
- dataset
- bool loaded_in
- accuracy
- loss
- f1 score
- description

methods
- init
- compare to databse
    
    

### run.py
file for running experiments
- run : loop through all attacks by calling evaluation_loop
    - options: which model, which attribution defense
    - returns *list* of class result
    - option to automatically save to database
- run_many : loop through list of attribution defenses and call run on each
    - return dict with key/value pairs of attribtuion name and list of class result
- evaluation_loop
    - option for attack
    - returns class result

### train.py
training loop function. should check every epoch for new highest accuracy on test set. If new highest accuracy is acheived it should automatically save a checkpoint to shared folder on drive. 

We should try to save some trained models that have close to state-of-the-art test set performance(i.e 99% MNIST, 90-95 cifar, would be cool to have some imagenet models). we might be able to just download some of these


### init.py
script to set up notebook
- clone github repo
- cd into github repo
- initialize global vars
- imports
- pip installs
- script accepts params to optionally automatically load a set of models in to run time

### utils.py
file for miscellaneous utility and helper functions

## Directory: Models
directory for implemeted models. sub directories for each dataset
- cifar10/resenet.py
- mnist/resnet.py
- imagenet/resnet.py
- etc

a file for loading models into run time
- load_models.py
    - creates model from .py files listed above then loads in check point from shared folder
    - params: list of (dataset, model name) tuples
    - return dict of loaded models

