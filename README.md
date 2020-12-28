# nlp-tagger-split

This repo contains the code for my NLP graduate course project.

## Categorizing and Tagging Words (Exercise 5-42)

**Purpose:** Investigate three different ways to define the split between training and testing data when developing a tagger using the Brown Corpus: genre (category), source (fileid), and sentence. Compare their relative performance and discuss which method is the most legitimate. You might use n-fold cross validation to improve the accuracy of the evaluations.

**Functionality:**

- The program uses a bigram tagger with the Brown Corpus as the dataset.
- The tagger is evaluated using three different methods of splitting the test/train datasets
- (by category, by fileid, and all sentences).
- The program evaluates performance when the train/test datasets are created from
- the same or different corpus sections (category, fileid).
- The program also evaluates performance using 10-fold cross-validation.

**Challenges:** There are a number of ways to evaluate performance, but I chose to keep it simple. It was a little difficult to implement 10-fold cross-validation since there were no code examples in the book to refer to.

## Compare their relative performance and discuss which method is the most legitimate.

The best performance occurred when splitting train/test on all sentences. This is most likely due to the fact that the tagger has a greater variety of context on which to train which could be considered the most "legitimate" approach.

When splitting by sentence within a single category versus two different categories, the performance changed by less than 1% (-0.2759%).

Taking all the sentences as a whole performed best. However, performance did not seem to change much with 10-fold cross-validation (-1.805%).

Output:

```
    train/test using same dataset:

    category: 0.872255489021956
    file:     0.7793880837359098
    sentence: 0.9227312326947461

    ambiguous_avg: 0.10994360529964245
    ambiguous_avg: 0.03275240384615385
    ambiguous_avg: 0.2550930740715241

    train/test using different datasets:

    category: 0.8419139119261768
    change:   -3.479%

    file:     0.6901408450704225
    change:   -11.45%

    sentence: 0.9201855058340367
    change:   -0.2759%

    train/test using same dataset with 10-fold cross-validation:

     1: 0.8721554116558742
     2: 0.8612371134020619
     3: 0.8137573663889454
     4: 0.8304923239809423
     5: 0.8331006979062812
     6: 0.8329007785985226
     7: 0.8256415786068578
     8: 0.8553958177744585
     9: 0.8427197160735967
    10: 0.8452476038338658
    category: 0.8412648408221406
    change:   -3.553%

     1: 0.7676282051282052
     2: 0.677762982689747
     3: 0.6557377049180327
     4: 0.7012195121951219
     5: 0.714095744680851
     6: 0.7120115774240231
     7: 0.7395209580838323
     8: 0.789198606271777
     9: 0.748335552596538
    10: 0.7283511269276394
    file:     0.7233861970915767
    change:   -7.185%

     1: 0.8875860001134512
     2: 0.8983687647193188
     3: 0.899540871057713
     4: 0.9158714232907611
     5: 0.9039128821770727
     6: 0.9087697086578238
     7: 0.9100761520326995
     8: 0.9146553953033488
     9: 0.9094234878751277
    10: 0.9125751765470128
    sentence: 0.9060779861774328
    change:   -1.805%
```
