---
title:   "2D perspective projection could introduce systematic error"
date:    2018-09-28 10:05:10 +0200
excerpt:
    If the camera is always placed to the left of the canvas, this could
    introduce small but consistent skewing of registered hit points to the
    right. Vice versa if the camera is always placed on the right of the
    canvas.
---
If the camera is placed arbitrarily but always to the left, then approximating
the hit position as the centroid of the puck could introduce small but
consistent skewing to the right.

<figure>
  <img src="{{ site.url }}{{ site.baseurl }}/assets/images/perspective-centroid-difference.png" alt="">
  <figcaption>
    Examples of perspective errors for different hit points when camera is
    aligned with the lower left of the canvas. Note reference centroid marked
    in blue. Personal illustration by author. September 2018.
  </figcaption>
</figure>

From the above figure, it can be seen that the camera perspective and 2D
projection make more of the flat sides of the pucks on the right visible,
causing the 2D centroid to move to the right. On the left side, due to the
camera angle being more head-on, the centroid will be a better approximation
to the actual position. Note also that the centroid of upper pucks also skew
up due to the camera being placed low.

It should be mentioned that the pucks usually has some spin and will hits the
canvas less clean than in the above case. If it hits broad side first, the
skewing is much less pronounced.

The effect can also be seen in the following figure

<figure>
  <img src="{{ site.url }}{{ site.baseurl }}/assets/images/wind-perspective-goal.jpg" alt="">
  <figcaption>
    Front and side view of canvas in windy conditions. The left side is
    aligned with the camera and therefore looks straight while the right side
    is curved due to the camera perspective. The side view shows that both
    sides curve approximately as much. Personal illustration by author.
    September 2018.
  </figcaption>
</figure>

One could argue that pucks hitting the canvas on the right comes in at an
angle, assuming the player is centered, and thus the puck would have moved
more to the right if the canvas had not stopped it early. However, assuming
this is a valid argument, the reverse would hold for the left side and then
the centroid would consistently skew to the right.

The best option is probably to alternate sides for the camera in order to
average it out over time.
