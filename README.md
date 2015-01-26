# compvis #

Computer vision routines in Python, based on Szeliski's "Computer Vision: Algorithms and Applications" (2011).

This library is mostly for my own learning purposes, since I find I understand concepts better after coding them out; but perhaps you might find something useful.

### Modules ###
* __examples__: Example scripts
  * __blend_orapple.py__: Blends an apple and orange using image pyramids
  * __match_features.py__: Matches Harris features in two images
* __feature__: Feature detection and matching (Szeliski chapter 4)
  * __detectors.py__: Feature detectors
  * __descriptors.py__ : Feature descriptors
* __imgform__: Image formation (Szeliski chapter 2)
  * __color.py__: Color spaces
  * __transforms.py__: Geometric transformations
* __imgproc__: Image processing (Szeliski chapter 3)
  * __filters__: Filters
    * __kernels.py__: Filter kernels
    * __linear.py__: Linear filters
    * __nonlinear.py__: Nonlinear filters
  * __imgproc.py__: General image processing
  * __pyramids.py__: Image pyramids
* __tests.py__: Unit tests
* __utils.py__: Miscellaneous utility functions

### Dependencies ###
* __numpy__
* __scipy__

For example scripts only:
* __matplotlib__
* __PIL__ (Python imaging library)
