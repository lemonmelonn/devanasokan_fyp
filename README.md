# devanasokan_fyp
Code repository for Final Year Project (Devan Asokan - Asia Pacific University)


### Possible Issues

Dataset size
Labelling prompt
Length of verses, maximum length
Proper LSTM approach, tuning
Unified tokenization for all models

### To Do (Components)

--- Model Training
- Tuning for other 3 models (need to test)
- Find optimal hyperparameter range
- Understand exact processes in model training/hyperparameter tuning notebooks
- Understand what is hidden size and attention heads in Bert and Distilbert


--- General
- Add callback to clear song label and song verses --- (done)
- Make only one csv for both explicit and non-explicit songs --- (done)
- See why cannot use LLM/ find out if still can use
- Make sure each song only has one set of lyrics, do not add if already exist
- Add monke pic? --- (done)
- Add logout feature? (remove cache)
- Proper name for dashboard
- Round up confidence score --- (done)

--- Manual Search Modal
- Adjust modal size (make it less wide)
- Adjust song card width in modal (make it smaller than modal to remove the bottom scroller)
- Button for manual search (opens modal) --- (done)
- Clear search bar after song selected --- (done)
- Update global variables after click song --- (done)
- Rename "currently_listening" layout to something general, can handle manual search and currently listening --- (done)

--- Touch Up
- Handle song info (label and verses) display when songs change, if same remain
- Handle songs with long choruses

--- After Finish All Features
- Redesign UI details
- Adjust width of column header (later, once all features are finalized)
- Adjust size of album cover
- Adjust position of "Get Report" button
- Display dataframe of verses (done)
- Add comments
- Remove any unused functions/code/styling


Structure of final report

Pipeline needs to be csv based, update line by line

Me


for my song card, there is a list is song cards

i want it to trigger when one of the cards are clicked