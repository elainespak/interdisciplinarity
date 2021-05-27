**Goal: Develop a measure of interdisciplinarity**

## 1. Compare university major's descriptions with the word embedding approach

Data:
* [National Center for Education Statistics (NCES) Classification of Instructional Programs (CIP) Codes](https://nces.ed.gov/ipeds/cipcode/browse.aspx?y=56) (scraped on May 18th, 2021)
* [CollegeBoard major and career](https://bigfuture.collegeboard.org/majors-careers) (scraped on May 7th, 2021)

Word embeddings:
* [fastText](https://fasttext.cc/docs/en/support.html): [wiki.en.bin](https://fasttext.cc/docs/en/pretrained-vectors.html)
* Word2Vec: [GoogleNews-vectors-negative300.bin.gz](https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit)
* SentenceBERT: [bert-base-nli-mean-tokens](https://github.com/UKPLab/sentence-transformers)

### Results
CollegeBoard + fastText:
* Average cosine similarity among **all** majors: 0.7577378195089631
* Average cosine similarity of **within-category1** majors: 0.7916725844257164
* Average cosine similarity of **within-category2** majors: 0.8343145892080468
* Average cosine similarity of **within-category3** majors: 0.8510020202228563

NCES + fastText:
* Average cosine similarity among **all** majors: 0.7378977994407522
* Average cosine similarity of **within-category1** majors: 0.8306243430865715
* Average cosine similarity of **within-category2** majors: 0.8539201886173065

NCES + Word2Vec:
* Average cosine similarity among **all** majors: 0.5575582608561134
* Average cosine similarity of **within-category1** majors: 0.7040585696085785
* Average cosine similarity of **within-category2** majors: 0.7529457843808666

## 2. Use traditional frameworks
* Biglan model
* The College Majors Finder (Rosen, Holmberg, & Holland, 1989)
* STEM vs. non-STEM distinction by DHS & NCES. [Link to the list](https://www.ice.gov/sites/default/files/documents/stem-list.pdf)
