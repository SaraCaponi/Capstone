#### Notes For Me

TODO Exploration

- Finalize project structure
- ngrams?
- VADER
- Confidence values
- scikit learn
  - LinearSVC
  - SGDClassifier
- Handle words with repetitive characters such as 'sweeeeeeeet'

#### Training Data

[Sentiment140 - 1.6 million tweets](https://www.kaggle.com/kazanova/sentiment140 "Kaggle")

Relevant Columns

- **target**: the polarity of the tweet (0 = negative, 4 = positive)
- **text**: the text of the tweet

#### Prepare Data

Assuming that your Python directory is rooted at Capstone.

```console
python svc/PrepareData.py --sample SAMPLE_PERCENTAGE
```

#### Training

##### Locally

TODO Document how to use hyperparameters

Assuming that your Python directory is rooted at Capstone.

```console
python svc/svc.py --model-dir svc/ --train svc/ --test svc/
```

##### On SageMaker

TODO Document how to train on SageMaker

#### Validating the Model

TODO Model validation metrics

### Invoking the Deployed Model

TODO Document how to invoke the deployed model

#### Input and Output Specifications

##### Input

```json
{
  "title": "Input Tweets",
  "description": "Tweets to be predicted",
  "type": "object",
  "properties": {
    "tweet": {
      "description": "An array of tweets",
      "type": "array",
      "items": {
        "type": "string"
      }
    }
  },
  "required": ["tweet"]
}
```

##### Output

```json
{
    "title": "Output predictions",
    "description": "Predictions input tweets",
    "type": "object",
    "properties" : {
        "results": {
            "description": "An array of prediction objects",
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "prediction": {
                        "type": "string",
                        "enum": ["NEGATIVE", "POSITIVE"]
                    },
                    "probability": {
                        "type": "array",
                        "items": "number"
                        "minItems": 2,
                        "maxItems": 2
                    }
                },
                "required": ["predictions", "probability"]
            }
        }
    }
    "required": ["results"]
}
```

#### Hyperparameter Tuning

TODO Hyperparameter tuning results

##### 2020/03/03

- 0.1 of the total data set
- Default hyperparameters

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
```

##### 2020/03/04

- 0.2 of the total data set
- Default hyperparameters

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
