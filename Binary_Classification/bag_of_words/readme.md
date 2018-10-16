Task- Distinguishing Intro frames from non-Intro frames

Method- Visual Bag of Words

Database- 55 TV show videos annotated with intro start and end timings

Protocol-
1) Random 75%-25% train-test split made to 55 videos. Led to 41 videos in training and 14 in testing.
2) For each of the video, positives frames (those lying in the intro) and negative frames (from 1 minute sequence in the video not lying in the intro) at 1 fps were collected and stored. So for both train and test videos, we have a set of positive and negative frames each.

Experiment- 
1) Took all the training frames, converted them to greyscale, resized them to a certain (w x h) ratio and labelled them 1 (positive) or 0 (negative).
2) Computed all the SIFT descriptors of each image and appended them to a list.
3) Clustered this list using KMeans to get a codebook (visual dictionary) of size 'k'.
4) With the codebook, we generate feature vectors for the training data using the SIFT descriptors again. This feature vector is of the size 'k' with the i-th element of the vector denoting how many descriptors of the image are close to the cluster centre i.
5) This feature vector along with the 0/1 labels fed into a linear SVM classifier.

6) We already have the learnt codebook and classifier. Using the testing frames, for each of them we generate a feature vector as mentioned above and label them 0/1.
7) Feed these feature vectors into the SVM classifier to get the outputs and compare them with the ground truth labels for accuracy.

Possible Hyperparameters-
1) (w x h) ratio
2) 'k' codebook size
3) SVM parameters like C (regularization)

Results-
1) Started with the orginial frame size without resizing and large k = 500. Major time spent in computing the SIFT features alone for each image and the overall time blows up and the algo doesn't run to completion.
2) Reduced the size by a factor 10 which was approximately (70 x 40) for each frame image, size of k still 500. Code runs successfully and the accuracy was 63.38%.
3) On varying both (w x h) ratio and 'k' codebook size, it turned out a much smaller 'k' gave better accuracy. So till now, the best obtained is 77.97% with (70 x 40) ratio and 'k = 32' as the codebook size.

References-
1) https://ianlondon.github.io/blog/how-to-sift-opencv/
2) https://ianlondon.github.io/blog/visual-bag-of-words/