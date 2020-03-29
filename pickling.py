"""
Using pickle for object-persistence.
"""
import pickle
from src_code import Hospital, Doctor, Nurse


def pickle_it():
    try:
        # create object
        details = Hospital('John Wick', 'Doctor')
        # create pickle file
        pickle_file = open('details', 'wb')
        # pickle the details and write it to the file
        pickle.dump(details, pickle_file)
        # close the file
        pickle_file.close()
    except ValueError as e:
        print(f'The exception is: {e}')


def un_pickle_it():

    try:
        # read the pickle file
        pickle_file = open('details', 'rb')
        # unpickle the data_frame
        details = pickle.load(pickle_file)
        # close pickle file
        pickle_file.close()

        # print the data_frame
        print(type(details))
        details.__str__()
    except FileNotFoundError:
        print('File not found')


if __name__ == "__main__":
    un_pickle_it()
