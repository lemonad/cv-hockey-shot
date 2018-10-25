---
title:   "Tenth Session: Artificial light"
date:    2018-10-25 12:50:10 +0200
---
Yesterday, I recorded seven rounds in artificial light. This is yet another
tricky situation I wanted to capture on video in order to later be able to
test for invariance. That a computer vision algorithm can be made invariant to
everything it is not supposed to detect or measure is never really the case,
especially in non-controlled situations like this.

Artificial light is problematic in several ways. For one, artificial light
is generally much more dim that natural light, which is why indoor photographs
often turn out blurred. A camera could try to counteract this by increasing
the aperture and increasing the sensitivity of the sensor but the latter
has the sideeffect of noisy images.

Secondly, artificial light usually causes hard shadows as the amount of
ambient light is so low compared to the point-source directed light. Thirdly,
the color temperature of artificial light is different from that of natural
light. This goes especially for street lighting and other similar sources of
light where the light quality is relatively unimportant to energy efficiency.

<figure>
  <img src="{{ site.url }}{{ site.baseurl }}/assets/images/puck-in-artificial-lighting.jpg" alt="">
  <img src="{{ site.url }}{{ site.baseurl }}/assets/images/puck-or-shadow.jpg" alt="">
  <figcaption>
    Two examples of ambiguous situations found in the recordings. [Left] The
    assumption that the puck is always darker than any part of the canvas
    is apparently not always true. [Right] It can be difficult to tell the
    puck from its shadow. October 2018.
  </figcaption>
</figure>

Last and most problematic, many light sources tend to pulse or flicker.
This is not always noticeable by eye but depending on type, these lights are
recharged/reignited according to the frequency, or twice the frequency,
of the power source. This is a known phenomena and one usually counteracts
it by recording in a frequency that divides twice the power source
frequency. Sweden has a power grid based on 50 hz and this means
that 20 hz, 33.33 or 50 hz is safe to use. One problem here is that at least
iPhones only offer multiple of 30 hz (since 60 hz is the power grid frequency
in the US, one can assume). So recording in the slo-mo mode and 120 hz causes
very noticeable pulsing as can be seen in the video below.

<figure>
  <iframe width="560" height="315"
          src="https://www.youtube.com/embed/_Z4O7aqLHNA" frameborder="0"
          allow="autoplay; encrypted-media" allowfullscreen></iframe>
  <figcaption>
    Strobe/rolling effect with artificial light in slow motion. Also note
    the amount of vertical canvas movement due to long distance between
    suspension points. Recorded with iPhone X in slo-mo 120 fps. October
    2018.
</figcaption>
</figure>

Augmenting the overhead lights with a sidemounted runner's headlamp seems to
have improved the situation but also caused canvas glare (see video below).

<figure>
  <iframe width="560" height="315"
          src="https://www.youtube.com/embed/7sySwrTLRUM" frameborder="0"
          allow="autoplay; encrypted-media" allowfullscreen></iframe>
  <figcaption>
    Using a side mounted runner's headlamp together with overhead artificial
    light. Recorded with iPhone X in slo-mo 120 fps (but video only initially
    runs in slow motion). October 2018.
</figcaption>
</figure>

Now, the benchmark comparison here is really human analysis of the video
material so if it is too dark to record a video, it would make it impossible
to accurately analyze and thus makes it out of scope for this study. The
accuracy in regards to these recordings definitely dropped because it was
dark, primarily because it was difficult to tell the puck from its shadow,
but it was by no means too dark.

With that said, from a training perspective, the light required to be able
to train is much less than to record the training. An existing training
location might thus have to be fitted with additional lights.

<figure>
  <img src="{{ site.url }}{{ site.baseurl }}/assets/images/20181024-example-result.png" alt="">
  <figcaption>
    The results from one of the seven rounds. October 2018.
  </figcaption>
</figure>

