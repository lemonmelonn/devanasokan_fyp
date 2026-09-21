# LyricLens: Implementing a Machine Learning Based Approach for Classifying Song Lyrics Appropriateness for Children

**Devan Asokan** | Final Year Project, Asia Pacific University

This project applies deep learning and transformer-based NLP (BERT) to evaluate song lyrics appropriateness for children, enabling safer listening experiences through contextual, verse-level content moderation. It covers the full pipeline — from data collection and LLM-assisted annotation, through model training and tuning, to a deployed model powering **LyricLens**, an interactive Spotify-connected dashboard.

`Text Classification` · `NLP` · `Lyrical Analysis` · `Content Moderation` · `SDG 3: Good Health and Well-being`

---

## Overview

Most content filters classify a song as a whole, which misses the reality that appropriateness often varies verse by verse. This project instead:

1. Collects songs and lyrics via the Spotify and Genius APIs
2. Splits lyrics into verses and uses an LLM to annotate each verse's appropriateness
3. Cleans and prepares the labelled verse-level dataset
4. Trains and tunes four model architectures (RNN, LSTM, BERT, DistilBERT) to classify verses
5. Deploys the best-performing model (BERT) to the Hugging Face Hub
6. Serves it through **LyricLens**, a dashboard that lets a user log in with Spotify and see verse-level appropriateness classifications for their music

## Pipeline

```
01_data_collection  →  02_LLM_annotation  →  03_data_cleaning  →  04_data_understanding
                                                                          │
                                                                          ▼
              07_lyriclens (dashbaord)   ←  06_model_deployment  ←  05_model_training
                                                          
```

## Repository Structure

| Folder | Description |
|---|---|
| `01_data_collection` | Scripts to pull songs from Spotify, detect song language, fetch lyrics from Genius, and split lyrics into verses |
| `02_LLM_annotation` | Notebook that uses an LLM (via Ollama) to label each verse's appropriateness |
| `03_data_cleaning` | Verse-level language detection, text cleaning, and final dataset preparation |
| `04_data_understanding` | Exploratory data analysis and visualizations of the labelled dataset |
| `05_model_training` | Initial training and hyperparameter tuning notebooks for four models: RNN, LSTM, BERT, DistilBERT. `trials/` holds earlier experiments not used in the final pipeline |
| `06_model_deployment` | Uploads the final trained model/tokenizer to the Hugging Face Hub and tests the deployed endpoint |
| `07_lyriclens` | The production Dash web app: Spotify login, verse-level lyric classification, and results dashboard |
| `requirements.txt` | Python dependencies for the full pipeline |

## Models

Four architectures were trained and tuned on the labelled verse dataset:

| Model | Notebook(s) |
|---|---|
| RNN | `model1_rnn_initial.ipynb`, `model1_rnn_tuning.ipynb` |
| LSTM | `model2_lstm_initial.ipynb`, `model2_lstm_tuning.ipynb` |
| BERT | `model3_bert_initial.ipynb`, `model3_bert_tuning.ipynb` |
| DistilBERT | `model4_distilbert_initial.ipynb`, `model4_distilbert_tuning.ipynb` |

Hyperparameter tuning was performed with **Optuna**. The final BERT model was selected for deployment and is hosted at [`devanasokan/bert-lyrics-classifier`](https://huggingface.co/devanasokan/bert-lyrics-classifier) on the Hugging Face Hub.

<!-- TODO: add final evaluation metrics (accuracy / F1 / precision / recall) comparing the four models -->

## Getting Started

### Prerequisites

- Python 3.10+
- A [Spotify Developer](https://developer.spotify.com/dashboard) app (Client ID/Secret) for OAuth login
- A [Genius API](https://genius.com/api-clients) client access token
- A [Hugging Face](https://huggingface.co/settings/tokens) account/token (only needed for `06_model_deployment`)
- [Ollama](https://ollama.com/) running locally (only needed for `02_LLM_annotation`)

### Installation

```bash
git clone https://github.com/lemonmelonn/devanasokan_fyp.git
cd devanasokan_fyp
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

If you plan to run the language-detection / cleaning steps, also download the required spaCy model:

```bash
python -m spacy download en_core_web_sm
```

### Environment variables

Create a `.env` file in the root directory:

```
CLIENT_ID=your_spotify_client_id
CLIENT_SECRET=your_spotify_client_secret
ACCESS_TOKEN=your_genius_access_token
HF_ACCESS_TOKEN=your_huggingface_token
```

### Running the dashboard

```bash
cd 07_lyriclens
python app.py
```

The app runs at `http://127.0.0.1:5000`. Log in with Spotify to view verse-level lyric classifications for your listening history.

### Reproducing the pipeline

The numbered folders (`01` → `06`) are intended to be run in order, since each stage consumes the output of the previous one:

1. `01_data_collection` – collect songs and lyrics
2. `02_LLM_annotation` – label verses
3. `03_data_cleaning` – clean and finalize the dataset
4. `04_data_understanding` – explore the data (optional, for analysis/reporting)
5. `05_model_training` – train and tune models
6. `06_model_deployment` – push the final model to the Hugging Face Hub

> Note: PyTorch model training notebooks in `05_model_training` require a kernel restart between training runs.

## Tech Stack

- **Data**: Spotipy, LyricsGenius, pandas, spaCy, langdetect, contractions
- **Annotation**: Ollama (local LLM)
- **Modeling**: PyTorch, Hugging Face Transformers/Datasets/Evaluate/Accelerate, scikit-learn, Optuna
- **Deployment**: Hugging Face Hub, ONNX Runtime
- **Dashboard**: Dash, Dash Bootstrap Components, Dash Mantine Components, Plotly, Flask

## License

This project is licensed under the MIT License — see [`LICENSE`](./LICENSE) for details.

## Author

**Devan Asokan**<br>
Final Year Project, Asia Pacific University