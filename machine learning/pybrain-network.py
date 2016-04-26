#Author :Zhu Zichen
#Date : 2016/4/5
import sys, os, getopt
import numpy as np
import pickle
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer


def output_model(ds, model_name, input_len, output_len):
    model_file = file(model_name, "wb")
    neural_network = buildNetwork(input_len, 500, output_len, bias=True)
    trainer = BackpropTrainer(neural_network, ds, weightdecay=0.1, learningrate=0.0001)
    trainer.trainEpochs(epochs=100)
    model_str = pickle.dumps(neural_network)
    pickle.dump(model_str, model_file, True)
    return neural_network


def file_train(filename, model_name):
    data = np.loadtxt(filename, float)
    input_info = data[1:][..., 0:-1]
    target = data[1:][..., [-1]]
    input_len = len(input_info[0])
    output_len = 1
    data_num = len(input_info)
    ds = SupervisedDataSet(input_len, output_len)
    for i in range(data_num):
        ds.addSample(input_info[i], target[i])
    neural_network = output_model(ds, model_name, input_len, output_len)
    return neural_network


def file_check(mode, filename, model_name="", neural_network={}):
    data = np.loadtxt(filename, float)
    if mode == 1:
        pass
    elif mode == 2 and neural_network == {} and os.path.exists(model_name):
        model_file = file(model_name, "rb")
        model_str = pickle.load(model_file)
        neural_network = pickle.loads(model_str)
    else:
        print "Invalid parameter"
        sys.exit()

    if os.path.exists(filename):
        data = np.loadtxt(filename, float)
        input_info = data[1:-1][..., 0:-1]
        target = data[1:-1][..., [-1]]
        input_len = len(input_info[0])
        output_len = 1
        data_num = len(input_info)

        ds = SupervisedDataSet(input_len, output_len)
        for i in range(data_num):
            ds.addSample(input_info[i], 0)
        print neural_network.activateOnDataset(ds)


def dir_train(dir_name, model_name):
    if os.path.exists(dir_name) :
        flag = True
        for parent, dirnames, filenames in os.walk(dir_name) :
            for filename in filenames :
                print filename
                data = np.loadtxt(os.path.join(dir_name, filename), float)
                input_info = data[1:][..., 0:-1]
                target = data[1:][..., [-1]]
                data_num = len(data)
                if flag:
                    flag = False
                    input_len = len(input_info[0])
                    output_len = 1
                    ds = SupervisedDataSet(input_len, output_len)
                for i in range(data_num):
                    ds.addSample(input_info[i], target[i])
        neural_network = output_model(ds, model_name, input_len, output_len)
        return neural_network
    else:
        print "Invalid directory name."
        sys.exit()


def dir_check(mode, dir_name, model_name="", neural_network={}):
    if mode == 1:
        pass
    elif mode == 2 and neural_network == {} and os.path.exists(model_name):
        model_file = file(model_name, "rb")
        model_str = pickle.load(model_file)
        neural_network = pickle.loads(model_str)
    else:
        print "Invalid parameter"
        sys.exit()

    if os.path.exists(dir_name) :
        for parent, dirnames, filenames in os.walk(dir_name) :
            for filename in filenames :
                data = np.loadtxt(os.path.join(dir_name, filename), float)
                input_info = data[1:-1][..., 0:-1]
                target = data[1:-1][..., [-1]]
                input_len = len(input_info[0])
                output_len = 1
                data_num = len(input_info)

                ds = SupervisedDataSet(input_len, output_len)
                for i in range(data_num):
                    ds.addSample(input_info[i], 0)
                print neural_network.activateOnDataset(ds)
    else:
        print "Invalid directory name."
        sys.exit()


if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "rct")
    directory_flag = False
    check_flag = False
    train_flag = False
    model_name = "model.pkl"
    for opt, value in opts:
        if opt == "-r":
            directory_flag = True
        elif opt == "-c":
            check_flag = True
        elif opt == "-t":
            train_flag = True
        else:
            pass
    if train_flag and len(args) >= 1:
        trained_data = args[0]
        if directory_flag:
            neural_network = dir_train(trained_data, model_name)
            if check_flag and len(args) == 2:
                check_data = args[1]
                dir_check(1, check_data, model_name, neural_network)
        else:
            neural_network = file_train(trained_data, model_name)
            if check_flag and len(args) == 2:
                check_data = args[1]
                file_check(1, check_data, model_name, neural_network)
    elif check_flag and len(args) == 1:
        check_data = args[0]
        if directory_flag:
            dir_check(2, check_data, model_name)
        else:
            file_check(2, check_data, model_name)
    else:
        print("Invalid parameters")
        sys.exit()
