TODO Document the SVC process.

Include: 
* How to train, test, and deploy the model both locally and to SageMaker.
* Input/Output specifications
* How to invoke the deployed model
* Hyperparameter tuning results

#### Training Locally
```console
python svc.py --model-dir ./ --train ./ --test ./
```

#### Hyperparameter Tuning
##### 2020/03/03
* 0.1 of the total data set.
* Default hyperparameters
```console
PS C:\Users\jaege\Desktop\SVM> python training.py --model-dir ./ --train ./ --test ./
Extracting arguments
Reading Tweets
Preprocessing the Tweets
Building training and testing datasets
0              prefer driving night much prettier
1        spells end richie takin tomorrow morning
2    wasting much time trying get internet access
3                                 sweeeeeeeeeeety
4                              college hot shorts
Name: text, dtype: object
0    POSITIVE
1    NEGATIVE
2    NEGATIVE
3    POSITIVE
4    POSITIVE
Name: target, dtype: object
Training the model
Print validation statistics
Accuracy Score: 0.76628125
Score: 0.76628125
Save the model
````

