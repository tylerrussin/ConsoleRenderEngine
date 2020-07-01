# Twitter Tweet Predictor Web Application
 

# Introduction
 
With the increase in data driven techniques being developed methods to integrate such models within web application environments is a vital necessity. Data flows through websites and with proper systems in place that data can be used to cater to the user experience or be extracted for the solving of real world problems. This demo application aims to be an example of this relationship. The system takes in data in real time from the twitter api and learns to predict which twitter user is most likely to say a given phrase. THis process uses Natural Language Processing to dissect text and logistic regression to make predictions
 
## Usage
 
Users can use the interactive front end to search any public twitter account and upload that account’s historical tweet data. Of the uploaded user accounts two users can then be selected, the model will then predict which user is most likely to say a provided tweet.

WARNING!!! the app uses free heroku services. Load times will be slow!!!
Check out the app [HERE!](https://tyler9937-twitoff.herokuapp.com/)


 
## Models used
 
This application uses a Logistic Regression model that is trained in real time on tokenized tweet data.
 
The following is a sample of the model’s code
 
```python
def predict_user(user1_name, user2_name, tweet_text):

    # Query Users
    user1 = User.query.filter(User.name == user1_name).one()
    user2 = User.query.filter(User.name == user2_name).one()

    # Process Data
    user1_embeddings = np.array([tweet.embedding for tweet in user1.tweets])
    user2_embeddings = np.array([tweet.embedding for tweet in user2.tweets])

    embeddings = np.vstack([user1_embeddings, user2_embeddings])
    labels = np.concatenate([np.ones(len(user1.tweets)),
                            np.zeros(len(user2.tweets))])

    # Fits Logistic Regression Model                      
    log_reg = LogisticRegression().fit(embeddings, labels)
    tweet_embedding = BASILICA.embed_sentence(tweet_text, model='twitter')

    return log_reg.predict(np.array(tweet_embedding).reshape(1,-1))
```
 
## License
[MIT](https://choosealicense.com/licenses/mit/)
 
