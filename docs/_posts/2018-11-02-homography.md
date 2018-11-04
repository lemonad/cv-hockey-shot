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
perfectly every time. A small fraction of the frames (out of thousands) has
intermittent homographies suddenly jumping to something like the below (and
then back again).

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

At first, this appeared to be a working fix but then I noticed that the
initial frame was bad for a round (see below). This caused the starting
points to be off and even though the Kalman filter slowly adjusted itself
to a good representation of the canvas corners, it took much more time
than the six frames I had alloted. Why not let it run 60 frames? Because
calculating the homography based on SIFT and brute force matching is a
choice of precision rather than processing time.

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
shots*. As long as the first homography in a whole session is okay, the
rest should be too.

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

For now, some of the bad cases, like the one above, can be handled by checking
that the corners resulting from the transformation are ordered properly
(the left corners having smaller x-coordinates than the right corners, etc.)
Also the ratio of side lengths should be within some margin. This does not
completely fix the problem but results in far fewer erroneous goal corners.

*Edit*: I also managed to improve things by adjusting the SIFT parameters
for the stencil based on it being an illustration. This is also something
I need to look into more as it is not obvious what an optimal set of
parameters look like for this application. Also, at this moment I can only
visually inspect the images -- and there are thousands.

*Edit 2*: The processing time for all session excepth the eleventh took 13
hours and 12 minutes. The result was 3441 examples of the puck just having
hit the canvas and 3519 examples of the canvas not yet having been hit. Based
on visual inspection, very few examples are based on a non-optimal homography
and none of the examples are invalid. The total, just shy of 7000 examples,
should be enough data for now.
