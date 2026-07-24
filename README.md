# devanasokan_fyp
Code repository for Final Year Project (Devan Asokan - Asia Pacific University) <br><br>


### Hyperparameter

Learning Rate
Weight Decay - regularization technique that prevents a machine learning model from becoming overly complex, overconfident, or memorizing training data (overfitting)
Training Batch Size

Warmup ratio?
Label smoothing?

Early stopping = 2, keep num_epochs constant


### Possible Issues

Labelling prompt
Length of verses, maximum length
Proper LSTM approach, tuning
Unified tokenization for all models <br><br>



### To Do (Components)
<br>

--- Model Training
- Tuning for other 3 models (need to test)
- No need k-fold, just use different ratios
- Understand exact processes in model training/hyperparameter tuning notebooks
- Understand what is hidden size and attention heads in Bert and Distilbert <br><br>

<br>
-- Try for DistilBERT first

- Why is validation loss keep increasing? IDK BREV
- Can BERT actually use epochs?
- Define different train, validation, test ratios
- Find optimal hyperparameter range
- Can i tune more hyperparameters? (only tuning 4 now)
- Add patience in trainer initialization
- Adjust number of epochs (5 or 10?)<br><br>


--- General
- See why cannot use LLM/ find out if still can use
- Make sure each song only has one set of lyrics, do not add if already exist
- Handle songs with long choruses
- Add logout feature? (remove cache)
- Add info at song label card --- (done)
- Add callback to clear song label and song verses --- (done)
- Make only one csv for both explicit and non-explicit songs --- (done)
- Add monke pic? --- (done)
- Round up confidence score --- (done)
- Handle song info (label and verses) display when songs change, if same remain --- (done) <br><br>



--- Manual Search Modal
- Button for manual search (opens modal) --- (done)
- Clear search bar after song selected --- (done)
- Update global variables after click song --- (done)
- Rename "currently_listening" layout to something general, can handle manual search and currently listening --- (done) <br><br>



--- Model Page
- Model overview
- Dataset used, statistics (songs, verses, label, distribution)
- Preprocessing steps
- Best Hyperparameters
- Confusion Matrix, Loss, Accuracy?
- Comparison with other model <br><br>



--- After Finish All Features
- Redesign UI
- Adjust song card text size
- Proper name for dashboard
- Adjust modal size (make it less wide)
- Adjust song card width in modal (make it smaller than modal to remove the bottom scroller)
- Adjust width of column header (later, once all features are finalized)
- Adjust size of album cover
- Adjust position of "Get Report" button
- Display dataframe of verses --- (done)
- Add code comments
- Remove any unused functions/code/styling <br><br>

