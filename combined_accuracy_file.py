import sprakbanken_evaluation
import prima_evaluation


def combined_accuracy_file(ocr_file, truth_file, output_file=False):
    outputArray = []
    outputArray.append("Evaluation for file: %s\n\n" % ocr_file)
    outputArray.append(
        "Prima evaluation:\n WordAccuracy: %s\t CharacterAccuracy:%s \n\n" % prima_evaluation.evaluate_file(ocr_file,
                                                                                                            truth_file))
    outputArray.append(
        "Språkbanken Evaluation Script:\n Word Errorrate: %s\t Character Errorrate: %s \n\n" % sprakbanken_evaluation.evaluate_file(
            ocr_file,
            truth_file))

    if (output_file):
        with open(output_file, 'w') as fd:
            for line in outputArray:
                fd.write(line)
    else:
        print(''.join(outputArray))
