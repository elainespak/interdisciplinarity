**Goal: Develop a measure of interdisciplinarity**

## 1. Compare university major's descriptions with the word embedding approach

Data:
* [National Center for Education Statistics (NCES) Classification of Instructional Programs (CIP) Codes](https://nces.ed.gov/ipeds/cipcode/browse.aspx?y=56)
* [CollegeBoard major and career](https://bigfuture.collegeboard.org/majors-careers) (scraped on May 7th)

Word embeddings:
* [fastText](https://fasttext.cc/docs/en/support.html)
* word2vec
* BERT

### Results
CollegeBoard + fastText:
* Average cosine similarity among **all** majors: 0.7577378195089631
* Average cosine similarity of **within-category1** majors: 0.7916725844257164
* Average cosine similarity of **within-category2** majors: 0.8343145892080468
* Average cosine similarity of **within-category3** majors: 0.8510020202228563

## 2. Use traditional frameworks
* Biglan model
* The College Majors Finder (Rosen, Holmberg, & Holland, 1989)
