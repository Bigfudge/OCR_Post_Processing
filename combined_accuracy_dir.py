import sprakbanken_evaluation
import prima_evaluation


def combined_accuracy_dir(ocr_dir, truth_dir, source, output_file=False):
    outputArray = []
    outputArray.append("Evaluation for directory: %s\n\n" % ocr_dir)
    outputArray.append(
        "Prima evaluation:\n WordAccuracy: %s\t CharacterAccuracy:%s \n\n" % prima_evaluation.evaluate_dir(ocr_dir,
                                                                                                           truth_dir,
                                                                                                           source))
    outputArray.append(
        "Språkbanken Evaluation Script:\n Word Errorrate: %s\t Character Errorrate: %s \n\n" % sprakbanken_evaluation.evaluate_dir(
            ocr_dir, truth_dir,
            source))
    if output_file:
        with open(output_file, 'w') as fd:
            for line in outputArray:
                fd.write(line)
    else:
        print(''.join(outputArray))
