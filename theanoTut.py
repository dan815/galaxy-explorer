from theano import tensor as T
import numpy as np
import theano
np.random.seed(42)
np.random.randn(4,3)

w=theano.shared(np.random.randn(4,3))
b=theano.shared(np.ones(3))
print(w)