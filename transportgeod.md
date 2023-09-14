---
layout: page
title: Transport geodesics
---

The concept of _transport geodesics_ was introduced in [[1] and [4]](/research.md). 
They are traces of individual masses that move along a sequence of optimal transport plans. 
All such traces turn out to be geodesics under the assumption that the concatenation of those transport plans is also optimal 
(i.e., triangle inequality for L<sup>1</sup>-Wasserstein metric holds with equality).
In short, transport geodesics are shortest paths which are constructed from optimal transport plans.

Here I draw transport geodesics on certain graphs. Masses are transported through a sequence of probability measures 1<sub>v<sub>0</sub></sub>,
&mu;<sub>v<sub>0</sub></sub>, &mu;<sub>v<sub>1</sub></sub>, ..., &mu;<sub>v<sub>n</sub></sub>, 1<sub>v<sub>n</sub></sub>, 
where v<sub>0</sub>,v<sub>1</sub>,...,v<sub>n</sub> is a diametral geodesic, and  1<sub>v</sub> is the dirac measure on v, and &mu;<sub>v</sub> is uniformly distributed measure on the ball of radius 1 around v.

<figure style="width:300px; float:left ; margin:0px; text-align:center; padding-right:32px;">	
<img src="/images/anim-4cube.gif" style="width:300;border:5px groove #D2691E" /> 
<figcaption>4-dimensional cube</figcaption>
</figure>

<figure style="width:300px; float:left; margin:0px; text-align:center; padding-left:32px;">
<img src="/images/anim-j84.gif" style="width:300;border:5px groove #DEB887" />
<figcaption>Johnson graph J(8,4)</figcaption>
</figure>

<figure style="width:700px; float:left; margin:0px; text-align:center; padding-left:32px;">
<img src="/images/ani-CPJ.gif" style="width:700;border:5px groove #DEB887" />
<figcaption>Product of cocktail party graph CP(4) and Johnson graph J(6,3)</figcaption>
</figure>
