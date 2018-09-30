---
title:   "Canvas has a non-planar homography in windy conditions"
date:    2018-09-29 21:19:10 +0200
excerpt:
    In windy conditions, the canvas becomes a curved surface rather than
    a plane and it becomes impossible to find other than a very approximative
    homography.
---
In windy conditions, the canvas becomes a curved surface rather than
a plane and it becomes impossible to find other than a rough approximation
of the homography.

<figure>
  <img src="{{ site.url }}{{ site.baseurl }}/assets/images/canvas-wind-non-planar.jpg" alt="">
  <img src="{{ site.url }}{{ site.baseurl }}/assets/images/canvas-wind-planar.jpg" alt="">
  <figcaption>
    The top image shows the canvas with wind from behind, causing the canvas
    to take on a curved, non-planar shape. Only a rough approximation of the
    planar homography can be found in this case. The bottom image shows the
    canvas when the wind has subdued temporarily, here the found homography
    more closely matches the shape of the goal region.
    Personal photos by author. September 2018.
  </figcaption>
</figure>

Since a mapping between the coordinate space of the canvas in the picture and
a rectangular and planar representation of the canvas (i.e. without
perspective) relies on finding a good homography, windy conditions provide
quite the challenge. Finding non-planar mappings is not impossible but seems
much less reliable.
