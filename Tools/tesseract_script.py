from subprocess import call
import os


def argus(input_dir, output, truthPath):
    truth = []
    for file in os.listdir(truthPath):
        truth.append(os.path.splitext(file)[0][-4:])
    print(len(truth))
    for file in os.listdir(input_dir):
        if os.path.splitext(file)[0][-4:] not in truth:
            print("skip")
            continue
        image = input_dir + file
        out = output + os.path.splitext(file)[0]
        print(image)
        print(out)
        call(["sudo", "tesseract", image, out, "-l", "swe-frak"])


def grepect(input_dir, output, truthPath):
    truth = []
    for file in os.listdir(truthPath):
        truth.append(os.path.splitext(file)[0])
    print(truth)
    for file in os.listdir(input_dir):
        if os.path.splitext(file)[0] not in truth:
            print("skip")
            continue
        image = input_dir + file
        out = output + os.path.splitext(file)[0]
        print(out)
        call(["tesseract", image, out, "-l", "swe-frak"])
