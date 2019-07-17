import constants as c
import helper_funtions as h
import subprocess
import platform

def	run_acc(genPath, truthPath, reportPath, frontierPath, command, source):
	pairOfPaths= get_pair(genPath, truthPath, source)
	count=0
	if len(os.listdir(reportPath) ) != 0:
		os.system('rm ' + reportPath+"*")
	for	item in pairOfPaths:
		if(len(item)<2):
			continue
		call([frontierPath+command,truthPath+item[1],genPath+item[0],
				reportPath+"accuracy_report_"+str(count)])

		count += 1

def	combinedAcc(reportPath, frontierPath, command, outputFile):
	all_reports = [report for report in glob.glob(reportPath + '/*')]
	command = [frontierPath+command] + all_reports
	p = subprocess.Popen(command,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	output, error = p.communicate()
	if error:
		print("ERROR", error)
	with open(outputFile, 'w') as fd:
		fd.write(output)

def completeEvaluation():
	run_acc(c.genOcropusArgus, c.truthArgus, c.charReportOcropusArgus, c.frontierPath, "accuracy", "Argus")
	run_acc(c.genOcropusGrepect, c.truthGrepect, c.charReportOcropusGrepact, c.frontierPath, "accuracy", "Grepect")
	run_acc(c.genTesseractArgus, c.truthArgus, c.charReportTesseractArgus, c.frontierPath, "accuracy", "Argus")
	run_acc(c.genTesseractGrepect, c.truthGrepect, c.charReportTesseractGrepect, c.frontierPath, "accuracy","Grepect")
	run_acc(c.genABBYYArgus, c.truthArgus, c.charReportABBYYArgus, c.frontierPath, "accuracy", "Argus")
	run_acc(c.genABBYYGrepect, c.truthGrepect, c.charReportABBYYGrepect, c.frontierPath, "accuracy","Grepect")

	run_acc(c.output_OcropusArgus, c.truthArgus, c.outputCharReportOcropusArgus, c.frontierPath, "accuracy", "Argus")
	run_acc(c.output_OcropusGrepect, c.truthGrepect, c.outputCharReportOcropusGrepact, c.frontierPath, "accuracy", "Grepect")
	run_acc(c.output_TesseractArgus, c.truthArgus, c.outputCharReportTesseractArgus, c.frontierPath, "accuracy", "Argus")
	run_acc(c.output_TesseractGrepect, c.truthGrepect, c.outputCharReportTesseractGrepect, c.frontierPath, "accuracy","Grepect")
	run_acc(c.output_ABBYYArgus, c.truthArgus, c.outputCharReportABBYYArgus, c.frontierPath, "accuracy", "Argus")
	run_acc(c.output_ABBYYGrepect, c.truthGrepect, c.outputCharReportABBYYGrepect, c.frontierPath, "accuracy","Grepect")

	combinedAcc(c.charReportOcropusArgus, c.frontierPath, "accsum", "CharAcc_OcropusArgus.txt")
	combinedAcc(c.charReportOcropusGrepact, c.frontierPath, "accsum", "CharAcc_OcropusGrepect.txt")
	combinedAcc(c.charReportTesseractArgus, c.frontierPath, "accsum", "CharAcc_TesseractArgus.txt")
	combinedAcc(c.charReportTesseractGrepect, c.frontierPath, "accsum", "CharAcc_TesseractGrepect.txt")
	combinedAcc(c.charReportABBYYArgus, c.frontierPath, "accsum", "CharAcc_ABBYYArgus.txt")
	combinedAcc(c.charReportABBYYGrepect, c.frontierPath, "accsum", "CharAcc_ABBYYGrepect.txt")

	combinedAcc(c.outputCharReportOcropusArgus, c.frontierPath, "accsum", "Output_CharAcc_OcropusArgus.txt")
	combinedAcc(c.outputCharReportOcropusGrepact, c.frontierPath, "accsum", "Output_CharAcc_OcropusGrepect.txt")
	combinedAcc(c.outputCharReportTesseractArgus, c.frontierPath, "accsum", "Output_CharAcc_TesseractArgus.txt")
	combinedAcc(c.outputCharReportTesseractGrepect, c.frontierPath, "accsum", "Output_CharAcc_TesseractGrepect.txt")
	combinedAcc(c.outputCharReportABBYYArgus, c.frontierPath, "accsum", "Output_CharAcc_ABBYYArgus.txt")
	combinedAcc(c.outputCharReportABBYYGrepect, c.frontierPath, "accsum", "Output_CharAcc_ABBYYGrepect.txt")


	run_acc(c.genOcropusArgus, c.truthArgus, c.wordReportOcropusArgus, c.frontierPath, "wordacc", "Argus")
	run_acc(c.genOcropusGrepect, c.truthGrepect, c.wordReportOcropusGrepact, c.frontierPath, "wordacc", "Grepect")
	run_acc(c.genTesseractArgus, c.truthArgus, c.wordReportTesseractArgus, c.frontierPath, "wordacc", "Argus")
	run_acc(c.genTesseractGrepect, c.truthGrepect, c.wordReportTesseractGrepect, c.frontierPath, "wordacc","Grepect")
	run_acc(c.genABBYYArgus, c.truthArgus, c.wordReportABBYYArgus, c.frontierPath, "wordacc", "Argus")
	run_acc(c.genABBYYGrepect, c.truthGrepect, c.wordReportABBYYGrepect, c.frontierPath, "wordacc","Grepect")

	run_acc(c.output_OcropusArgus, c.truthArgus, c.outputWordReportOcropusArgus, c.frontierPath, "wordacc", "Argus")
	run_acc(c.output_OcropusGrepect, c.truthGrepect, c.outputWordReportOcropusGrepact, c.frontierPath, "wordacc", "Grepect")
	run_acc(c.output_TesseractArgus, c.truthArgus, c.outputWordReportTesseractArgus, c.frontierPath, "wordacc", "Argus")
	run_acc(c.output_TesseractGrepect, c.truthGrepect, c.outputWordReportTesseractGrepect, c.frontierPath, "wordacc","Grepect")
	run_acc(c.output_ABBYYArgus, c.truthArgus, c.outputWordReportABBYYArgus, c.frontierPath, "wordacc", "Argus")
	run_acc(c.output_ABBYYGrepect, c.truthGrepect, c.outputWordReportABBYYGrepect, c.frontierPath, "wordacc","Grepect")

	combinedAcc(c.wordReportOcropusArgus, c.frontierPath, "wordaccsum", "WordAcc_OcropusArgus.txt")
	combinedAcc(c.wordReportOcropusGrepact, c.frontierPath, "wordaccsum", "WordAcc_OcropusGrepect.txt")
	combinedAcc(c.wordReportTesseractArgus, c.frontierPath, "wordaccsum", "WordAcc_TesseractArgus.txt")
	combinedAcc(c.wordReportTesseractGrepect, c.frontierPath, "wordaccsum", "WordAcc_TesseractGrepect.txt")
	combinedAcc(c.wordReportABBYYArgus, c.frontierPath, "wordaccsum", "WordAcc_ABBYYArgus.txt")
	combinedAcc(c.wordReportABBYYGrepect, c.frontierPath, "wordaccsum", "WordAcc_ABBYYGrepect.txt")

	combinedAcc(c.outputWordReportOcropusArgus, c.frontierPath, "wordaccsum", "Output_WordAcc_OcropusArgus.txt")
	combinedAcc(c.outputWordReportOcropusGrepact, c.frontierPath, "wordaccsum", "Output_WordAcc_OcropusGrepect.txt")
	combinedAcc(c.outputWordReportTesseractArgus, c.frontierPath, "wordaccsum", "Output_WordAcc_TesseractArgus.txt")
	combinedAcc(c.outputWordReportTesseractGrepect, c.frontierPath, "wordaccsum", "Output_WordAcc_TesseractGrepect.txt")
	combinedAcc(c.outputWordReportABBYYArgus, c.frontierPath, "wordaccsum", "Output_WordAcc_ABBYYArgus.txt")
	combinedAcc(c.outputWordReportABBYYGrepect, c.frontierPath, "wordaccsum", "Output_WordAcc_ABBYYGrepect.txt")


#TODO Add metods for evaluate_file and evaluate_dir
