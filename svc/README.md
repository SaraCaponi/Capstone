#### Notes For Me

TODO Exploration

- Finalize project structure
- test_train_split
  - shuffle
  - stratify
- Handle words with repetitive characters such as 'sweeeeeeeet'
- Add more training data that isn't twitter related?
  - Stanford sentiment treebank data

#### Training Data

[Sentiment140 - 1.6 million tweets](https://www.kaggle.com/kazanova/sentiment140 "Kaggle")

Relevant Columns

- **target**: the polarity of the tweet (0 = negative, 4 = positive)
- **text**: the text of the tweet

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
                        "type": "number",
                    }
                },
                "required": ["predictions", "probability"]
            }
        }
    },
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