**Goal: Develop a measure of interdisciplinarity**

## 1. Compare university major's descriptions with the word embedding approach

Data:
* [CollegeBoard major and career](https://bigfuture.collegeboard.org/majors-careers) (scraped on May 7th)

Word embeddings:
* [fastText](https://fasttext.cc/docs/en/support.html)
  - Average cosine similarity among **all** majors: 0.7577378195089631
  - Average cosine similarity of **within-category1** majors: 0.7916725844257164
  - Average cosine similarity of **within-category2** majors: 0.8343145892080468
  - Average cosine similarity of **within-category3** majors: 0.8510020202228563
* word2vec
* BERT

## 2. Use traditional frameworks
* Biglan model
