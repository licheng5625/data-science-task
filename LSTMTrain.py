# Small LSTM Network to Generate Text for Alice in Wonderland
import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras import callbacks
from keras.utils import np_utils
# load ascii text and covert to lowercase
filename = "Charpter 1-3.txt"

evaluatefilename = "Chapter4 part.txt"
raw_text = open(filename).read()
raw_text = raw_text.lower()
raw_text_test = open(evaluatefilename).read()
raw_text_test = raw_text_test.lower()
# create mapping of unique chars to integers
chars = sorted(list(set(raw_text)))
char_to_int = dict((c, i) for i, c in enumerate(chars))
chars_test = sorted(list(set(raw_text_test)))
char_to_int_test = dict((c, i) for i, c in enumerate(chars_test))


# summarize the loaded data
n_chars = len(raw_text)
n_vocab = len(chars)
print("Total Characters: ", n_chars)
print("Total Vocab: ", n_vocab)
# prepare the dataset of input to output pairs encoded as integers
seq_length = 100
dataX = []
dataY = []
testdataX = []
testdataY = []
for i in range(0, n_chars - seq_length, 1):
	seq_in = raw_text[i:i + seq_length]
	seq_out = raw_text[i + seq_length]
	dataX.append([char_to_int[char] for char in seq_in])
	dataY.append(char_to_int[seq_out])

for i in range(0, len(raw_text_test) - seq_length, 1):
	seq_in = raw_text_test[i:i + seq_length]
	seq_out = raw_text_test[i + seq_length]
	testdataX.append([char_to_int[char] for char in seq_in])
	testdataY.append(char_to_int[seq_out])
n_patterns = len(dataX)
print("Total Patterns: ", n_patterns)
print("Total Patterns for test: ", len(testdataX))

# reshape X to be [samples, time steps, features]
X = numpy.reshape(dataX, (n_patterns, seq_length, 1))
# normalize
X = X / float(n_vocab)
# one hot encode the output variable
y = np_utils.to_categorical(dataY)

testX = numpy.reshape(testdataX, (len(testdataX), seq_length, 1))
testX = testX / float(n_vocab)
testY = np_utils.to_categorical(testdataY,nb_classes =47)



# define the LSTM model
model = Sequential()
model.add(LSTM(256,dropout_U=0.2, input_shape=(X.shape[1], X.shape[2]),return_sequences=True))
model.add(LSTM(256,dropout_U=0.2))
model.add(Dense(y.shape[1], activation='softmax'))
filename = "weights-improvement-00-1.6843.hdf5.2layer"
model.load_weights(filename)

model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
# define the checkpoint
filepath="weights-improvement-{epoch:02d}-{loss:.4f}.hdf5.2layer"
checkpoint = callbacks.ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
earlyStopping = callbacks.EarlyStopping(monitor='val_loss', patience=0, verbose=0, mode='auto')
callbacks_list = [checkpoint,earlyStopping]
# fit the model
model.fit(X, y, validation_data=(testX, testY) ,nb_epoch=20, batch_size=128, callbacks=[checkpoint,earlyStopping])
score, acc = model.evaluate(testX, testY,
                            batch_size=128)
print('Test score:', score)
print('Test accuracy:', acc)