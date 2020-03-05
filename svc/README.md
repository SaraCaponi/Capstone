TODO How to train, test, and deploy the model both locally and to SageMaker.

TODO Input/Output specifications

TODO How to invoke the deployed model

TODO Hyperparameter tuning results

TODO Model validation metrics

#### Notes For Me
TODO Exploration
* Finalize project structure
* ngrams?
* VADER
* Confidence values
* scikit learn
    * LinearSVC
    * SGDClassifier
* Handle words with repetitive characters such as 'sweeeeeeeet'

#### Training Locally
Assuming that your Python directory is rooted at Capstone. 
```console
python svc/svc.py --model-dir svc/ --train svc/ --test svc/
```

#### Hyperparameter Tuning
##### 2020/03/03
* 0.1 of the total data set
* Default hyperparameters
```console
PS C:\Users\jaege\Desktop\SVM> python training.py --model-dir ./ --train ./ --test ./
Extracting arguments
Reading Tweets
Preprocessing the Tweets
Training the model
Print validation statistics
Accuracy Score: 0.76628125
Score: 0.76628125
Save the model
````

##### 2020/03/04
* 0.2 of the total data set
* Default hyperparameters
```console
PS C:\Users\TSO7416\Desktop\Capstone\svc> python svc.py --model-dir ./ --train ./ --test ./
Extracting arguments
Reading Tweets
Length of train_df: 256000
Length of test_df: 64000
Preprocessing the Tweets
Building training and testing datasets
Training the model
Print validation statistics
Accuracy: 0.77115625
Precision: 0.7717396683801709
Recall: 0.77115625
Save the model
```

