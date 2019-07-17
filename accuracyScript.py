import os
import constants as c
import sprakbanken_evaluation
import prima_evaluation
import helper_funtions as h

def combined_accuracy_file(ocr_file, truth_file, output_file=False):
	outputArray=[]
	outputArray.append("Evaluation for file: %s\n\n" % ocr_file)
	outputArray.append("Prima evaluation:\n WordAccuracy: %s\t CharacterAccuracy:%s \n\n" % prima_evaluation.evaluate_file(ocr_file, truth_file))
	outputArray.append("Språkbanken Evaluation Script:\n Word Errorrate: %s\t Character Errorrate: %s \n\n" % sprakbanken_evaluation.evaluate_file(ocr_file, truth_file))

	if(output_file):
		with open(output_file, 'w') as fd:
			for line in outputArray:
				fd.write(line)
	else:
		print(''.join(outputArray))

def combined_accuracy_dir(ocr_dir, truth_dir, source, output_file=False):
	outputArray=[]
	outputArray.append("Evaluation for directory: %s\n\n" % ocr_dir)
	outputArray.append("Prima evaluation:\n WordAccuracy: %s\t CharacterAccuracy:%s \n\n" % prima_evaluation.evaluate_dir(ocr_dir, truth_dir,source))
	outputArray.append("Språkbanken Evaluation Script:\n Word Errorrate: %s\t Character Errorrate: %s \n\n" % sprakbanken_evaluation.evaluate_dir(ocr_dir, truth_dir,source))

	if(output_file):
		with open(output_file, 'w') as fd:
			for line in outputArray:
				fd.write(line)
	else:
		print(''.join(outputArray))

def combined_accuracy_report():
	combined_accuracy_dir(c.output_OcropusArgus, c.truthArgus, "Argus", os.path.join(c.working_folder,"AccuracyReportOcropusArgus.txt"))
	combined_accuracy_dir(c.output_OcropusGrepect, c.truthGrepect, "Grepect", os.path.join(c.working_folder,"AccuracyReportOcropusArgus.txt"))
	combined_accuracy_dir(c.output_TesseractArgus, c.truthArgus, "Argus", os.path.join(c.working_folder,"AccuracyReportTesseractArgus.txt"))
	combined_accuracy_dir(c.output_TesseractGrepect, c.truthGrepect, "Grepect", os.path.join(c.working_folder,"AccuracyReportTesseractGepect.txt"))
	combined_accuracy_dir(c.output_ABBYYArgus, c.truthArgus, "Argus", os.path.join(c.working_folder,"AccuracyReportABBYYArgus.txt"))
	combined_accuracy_dir(c.output_ABBYYGrepect, c.truthGrepect, "Grepect", os.path.join(c.working_folder,"AccuracyReportABBYYGrepect.txt"))
