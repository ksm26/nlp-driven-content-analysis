# Automated Web Article Analysis Pipeline

## Overview

This project implements an automated pipeline for extracting, processing, and analyzing textual content from web articles listed in an Excel file. The core functionalities include:

- Web scraping of article content using Selenium.
- Text preprocessing and cleaning.
- Sentiment analysis and readability metric computation.
- Structured output generation in Excel format.

---

## 📌 Project Objective

To extract article content from a list of URLs and compute various Natural Language Processing (NLP) metrics such as sentiment scores, readability indices, and text complexity, outputting the results in a well-defined structure.

---

## 🧠 Components

### 1. Data Extraction (`data_extraction.py`)

#### Features:
- Uses Selenium with headless Chrome for web scraping.
- Extracts clean article titles and main content from webpages.
- Filters out navigation, advertisements, and footers.
- Saves each article as a text file in the `extracted_articles/` directory.

#### Tools Used:
- `selenium`
- `pandas`
- `openpyxl`
- `webdriver-manager`

### 2. Sentiment & Readability Analysis (`sentiment_analysis.py`)

#### Features:
- Computes:
  - **Sentiment Scores:** Positive, Negative, Polarity, Subjectivity.
  - **Readability Metrics:** FOG Index, Average Sentence Length, Word Complexity, etc.
- Uses spaCy for text processing and custom logic for metrics.
- Outputs results in the format defined by `Output Data Structure.xlsx`.

#### Tools Used:
- `spaCy` with `en_core_web_sm`
- `pandas`
- `openpyxl`
- `re`

---
## 📂 Directory Structure
project-root/ \
├── extracted_articles/ # Stores extracted article .txt files \
├── MasterDictionary/ # Contains positive-words.txt and negative-words.txt \
├── StopWords/ # Directory with multiple stopword lists \
├── Input.xlsx # Contains URL_ID and URL  \
├── Output Data Structure.xlsx # Template for final output  \
├── data_extraction.py # Script to extract articles from URLs  \
├── sentiment_analysis.py # Script to compute text metrics 


---

## ✅ Setup Instructions

1. **Install dependencies:**

```bash
pip install selenium pandas openpyxl webdriver-manager spacy
python -m spacy download en_core_web_sm
```

2. **Run article extraction:**

Make sure Input.xlsx is present in the same directory.
```bash
python data_extraction.py
```

3. **Run sentiment analysis:**

Ensure extracted_articles/, MasterDictionary/, and StopWords/ directories are in place.
```bash
python sentiment_analysis.py
```

## 📊 Output
Results will be saved in a new Excel file based on the structure in Output Data Structure.xlsx.

Metrics calculated per article include:

| Metric                  | Description                                                    |
|-------------------------|----------------------------------------------------------------|
| Positive/Negative Score | Count of sentiment-associated words                            |
| Polarity Score          | Balance of sentiment                                           |
| Subjectivity Score      | Proportion of opinion-based content                            |
| FOG Index               | Readability measure based on word and sentence complexity      |
| Avg Sentence Length     | Average number of words per sentence                           |
| Complex Word Count      | Number of words with >2 syllables                              |
| Personal Pronouns       | Count of words like "I", "we", "my", etc.                      |
| Avg Word Length         | Mean character count per word                                  |
