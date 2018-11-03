---
title:   "Extracting an image of the goal in each video frame"
date:    2018-11-02 10:20:10 +0200
---
My initial working assumption was that I could exclude the part of finding
the exact location of the goal/canvas in each frame as
1. it is of secondary importance to the main problem of approximating the hit
  time,
2. surely, it can be done given that one spends time on the problem, and
3. I could use a manually positioned rectangular cropping area for each round
   of shots as both canvas and camera is stationary for each round, thus
   exluding most background interference.

Although (1) and (2) still hold, (3) barely even held for indoor sessions
where most parameters were fixed for the recording duration and definitely
does not hold for uncontrolled outdoor sessions. An underlying idea of using
a canvas is to provide something flexible and portable for players, which
comes with the side effect of less rigidity. On the other hand, few materials
hold up to being hit by a hockey puck in full speed (even expensive
match-quality hockey goals become dented) so non-rigid materials and mounting
methods is also a way of handling this.

The problem, then, is to find a transformation matrix (a homography) that
maps coordinates in the below canvas illustration to coordinates in an actual
video frame.

<figure>
  <img src="{{ site.url }}{{ site.baseurl }}/assets/images/canvas-stencil-adj-top-1cm.png"
       alt="">
  <figcaption>
    The canvas we want to find. Personal illustration by author, September 2018.
  </figcaption>
</figure>

In short, I use SIFT feature detection on both illustration and video frame
to find keypoints that can be used to match the two. I then use a brute force
matcher to find the set of most similar keypoints, which then is used to
construct a matching homography matrix using RANSAC. Then this is used to
construct a mask representing the corners of the canvas in order to extract
only the part of the canvas representing the goal, with very little background
visible.

The problem, like so often in computer vision, is that this does not work
perfectly every time. For a few intermittent frames out of thousands, the
homography suddenly jumped to something like the below.

<figure>
  <img src="{{ site.url }}{{ site.baseurl }}/assets/images/bad-homography.jpg"
       alt="">
  <img src="{{ site.url }}{{ site.baseurl }}/assets/images/bad-homography-masked.png"
       alt="">
  <figcaption>
    A non-optimal mapping between canvas coordinates and video frame
    coordinates (top) resulting in the masked image on the bottom.
    Personal illustration by author, November 2018.
  </figcaption>
</figure>

One solution could be to use the average corner coordinates over a number of
frames in order to even out the effects of these bad homographies. However,
what if one frame was really bad, like shown below? Then instead of having
one bad set of corner coordinates, all coordinates based on an average that
included the bad frame would be poor.

A better solution seems be to use something like Kalman filtering for each
corner, adjusting the parameters so the coordinates would adjust slowly and
big jumps would be treated as sensor errors. So I implemented this and let
the kalman filtering run for six frames before using the homography to
capture any example. I also reset the kalman filter after having processed
each shot since the canvas could potentially be repositioned by the player
in between each shot.

This fixed almost all problems but, of course, one of the initial frames was
bad, which can be seen below. This causes the initial position to be off
and even though the Kalman filter slowly adjusts itself to a good representation
of the canvas corners, this takes much more time than the six frames I had
alloted. Why not let it run 60 frames? Because calculating the homography
based on SIFT and brute force matching is a choice of precision rather than
processing time.

<figure>
  <img src="{{ site.url }}{{ site.baseurl }}/assets/images/bad-initial-homography.png"
       alt="">
  <figcaption>
     Masked image resulting from a bad initial homography. Personal illustration
    by author, November 2018.
  </figcaption>
</figure>

At this point, I adjusted my assumptions and instead of letting every shot
being independently analyzed and use the same Kalman filter over the whole
round of shots. Doubling the number of prior frames used should be enough
to adjust to reasonable changes in positions of tripod and canvas *between
shots*.

One might imagine that using more prior shots would be better, right? Not
entirely. One of the prior frames resulted in the below homography, from which
the kalman filter did not recover during the shot. A very similar problem
to the one discussed in relation to using the average over several frames.
In some sense this brings the whole problem **back to square one**.

<figure>
  <img src="{{ site.url }}{{ site.baseurl }}/assets/images/invalid-homography.jpg"
       alt="">
  <figcaption>
     An invalid homography for this application. Personal illustration by
     author, November 2018.
  </figcaption>
</figure>

In the long run, I probably need to experimentally find out what a reasonable
homography is. That is, for example, look into the range of plane normals
that can be expected given a mobile camera on a tripod, the canvas level
and hanging some distance off the ground.

For now, the above, worst-case, homography can be handled by checking that the
rotational part of the homography matrix has a positive determinant, which
essentially means that the transformation will preserve the order of the
corners.
