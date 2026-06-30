# Libraries used for data collection and preprocessing
import pandas as pd
import os
import lyricsgenius
from dotenv import load_dotenv
from tqdm import tqdm
import re
from transformers import pipeline
import contractions
import spacy
from langdetect import detect
import ast
import time
import json
import ollama



