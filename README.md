# This is a simple set of codes to help you get the pictures of your coin collection cropped up and centered

As is the case with most other non-ML CV algorithms, no one shoe fits all the sizes. I found coinSegment.py to give almost perfect results on my foreign coin collection, but about 50% accuracy on my Indian Coin Collection (which has a lot more aluminium coins). At the same time, coinSegment3.py, which had an accuracy of about 60% on my foreign coins gave near perfect results for my Indian coins.
coinSegment2.py serves no purpose and is incomplete, as of now

So feel free to experiment and come out with the best output

You will need OpenCV to run this code. To run it, place all your images in a folder, say 'TestFolder', then shoot up your terminal and enter
```bash
$ python coinSegment.py TestFolder
```
A sub-folder 'corrected' will be created inside 'TestFolder', which will contain the centered and cropped images

