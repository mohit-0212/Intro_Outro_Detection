Task- Detecting intro sequence timings of the second video, given we have 2 videos of the same show.

Experiment- 
1) Compute scene transition timings and generate the corresponding frames for the two videos.
2) Generate hashes of each individual scene transition frame obtained.
3) Compare the hashes of the two videos to get points where the hash matches. These match points will represent the times where the intro sequence frame can be found at in the second video.

Intuition-
1) Two episodes of the same TV show will most likely have the same intro sequence and we can match these sequences to get the timings for second video given we have one. 
