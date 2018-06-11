Task- Distinguishing Intro frames from non-Intro frames

Method- Feature vector extraction using vgg-16 fc layer and classification

Database- 55 TV show videos annotated with intro start and end timings

Protocol-
1) Random 75%-25% train-test split made to 55 videos. Led to 41 videos in training and 14 in testing.
2) For each of the video, positives frames (those lying in the intro) and negative frames (from 1 minute sequence in the video not lying in the intro) at 1 fps were collected and stored. So for both train and test videos, we have a set of positive and negative frames each.

Experiment- 
1) Took all the training frames, resized them to (224 x 224) ratio (standard for vgg classifier) and labelled them 1 (positive) or 0 (negative).
2) Passed all the training frames through vgg-16 network pretrained on Imagenet and extracted the last fc layer as the feature vector.
3) With these feature vectors along with the 0/1 labels were fed into a linear SVM classifier.

4) We now have the learnt classifier. Using the testing frames, for each of them we generate a feature vector as mentioned above using the vgg-16 network and label them 0/1.
5) Feed these feature vectors into the SVM classifier to get the outputs and compare them with the ground truth labels for accuracy.

Possible Hyperparameters-
1) SVM parameters like C (regularization)

Results-
1) An accuracy of ~87% obtained on the testing frames.

Cons-
1) Takes a lot of time for the forward pass of an image frame, so using all the image frames and doing a forward pass would blow up the time.

