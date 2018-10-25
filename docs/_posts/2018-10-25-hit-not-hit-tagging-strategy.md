---
title:   "Rules for annotating images as hits and non-hits"
date:    2018-10-25 23:25:10 +0200
---
In most cases there is an obvious difference between the canvas before
having being hit by a puck and after. The question, raised in a
[previous post]({% post_url 2018-10-25-artificial-light-invariance %}),
is how to deal with the edge cases.

There are basically five different three-sequence cases, all sharing

* frame *n-1*: the puck has yet to hit the canvas and is a good example of
  the class `not hit`.

##### Case 1 (the normal case)
* frame *n*: it is visually obvious that the puck has hit the canvas and
  provides a good example of the `hit` class.
* frame *n+1*: also a good example of the class `hit`, albeit not necessarily
  a good example of a puck *just* having hit the canvas.

##### Case 2 (hit provides bad training example)
* frame *n*: it is visually obvious that the puck has hit the canvas but it
  is likely a bad training example of the `hit` class based on the similarity
  with images of pucks very close to hitting the canvas (the `not hit` class),
* frame *n+1*: image provides a good example of the `hit` class.

##### Case 3 (ambiguous class)
* frame *n*: the puck could have or probably hit the canvas but it is
  uncertain. Thus, we do not know with certainty which training class to
  assign the image,
* frame *n+1*: it is visually obvious that the puck has hit the canvas and
  provides a good example of the `hit` class.

##### Case 4 (the miss)
* frame *n*: it is visually obvious that the puck has hit the canvas but
  since it hit outside the goal area, it does not necessarily provide a good
  example of the class `hit` (especially if the puck just grazed the edge of
  the canvas).

##### Case 5 (the bounce)
* frame *n*: it is visually obvious that the puck has hit the canvas but
  since it bounced beforehand and lost energy, it does not necessarily
  provide a good example of the class `hit` (sometimes it does and sometimes
  it does not).

Avoiding false positives must be the priority since identifying an image as
a hit when it is not could result in very bad measurements as the puck could
be far from its eventual impact point, perhaps not even visible in the
image. Missed identifications are less problematic as there will be a sequence
of images showing the puck having hit the canvas and it will be a slow and
gradual decrease in accuracy with later frames. Thus, we want to err on the
safe side and not include frames if they are not visually distinct enough.

After a puck hits the canvas, with each frame, the movement of the canvas
becomes less and less similar to the movement after first impact. Eventually
it turns into something that bears resemblence to the effects of strong wind.
Thus, we also want to avoid assigning later frames as examples of the class
`hit`.

Based on the above, a set of tentative rules for assigning classes are:

1. Prefer clear examples over poor or ambiguous examples,
2. Assign class `ambiguous` to frames in between clear examples in order to
   skip these frames for now,
3. Only assign a few (two–three) frames to class `hit` so the examples
   provide clear examples of the puck just having hit the canvas,
4. If miss, make no class assignments at this time,
5. If bounce, make the call for each case (it will be possible to exclude
   all examples for this case if needed).
