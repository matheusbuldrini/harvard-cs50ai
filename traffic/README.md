As a starting point, I used a neural network similar to the one presented in the 
lecture. It was not good, so I started to play around with the values for each 
layer. I fixed the random seed so I could compare different values better. Just 
for fun and experimentation, I set all values to a high number and let it run 
for an extended period. The results were better, but it was taking too much time. 
I tried different activation functions but noticed that 'ReLU' was working the 
best, so I kept it. After a few more trials, I looked at a TensorFlow tutorial 
about image classification available at https://www.tensorflow.org/tutorials/images/classification. 
I saw that they used multiple convolutional layers, so I decided to try 
increasing the number of convolutional layers.

First, I added one more convolutional layer, making it equal to the first one. 
The accuracy increased to about 87%. Convolutional layers seemed to have a good 
impact on the results, so I tried adding more convolutional layers with MaxPooling 
between each of them. However, it didn't work that well, so I stuck with 2 layers 
and played with the number of filter values, finding that 32 worked well for me. 
After tuning the convolutional layers, I tried adding one more hidden layer, and 
it worked well, so I tried adding one more. The results did not improved, so I 
kept the 2 hidden layers. Out of curiosity, I added one more convolutional layer, 
but it didn't help. After numerous trials and errors with different filter kernel 
sizes, pool sizes, and hidden layers, I achieved the best results using 2 
convolutional layers with MaxPooling between them and 2 hidden layers with dropout. 
I ran the code multiple times, and the results showed around 95% accuracy.