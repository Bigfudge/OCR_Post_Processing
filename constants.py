verbose = False

word_freq_path = "models/word_freq.pkl"

data_filepath = "./data"
models_filepath = "./models"
output_filepath = "/output"

error_words_TesseractArgus = 'error_words_TesseractArgus'
error_words_TesseractGrepect = 'error_words_TesseractGrepect'
error_words_OcropusArgus = 'error_words_OcropusArgus'
error_words_OcropusGrepect = 'error_words_OcropusGrepect'
error_words_ABBYYArgus = 'error_words_ABBYYArgus'
error_words_ABBYYGrepect = 'error_words_ABBYYGrepect'

word_features = ["word", "alfanumeric", "trigram", "word_freq", "vowel", "word_length", "ocr_output__num_upper", "has_number", "valid"]

training_data = "models/training_data.pkl"
svm_model = "models/svm_model.pkl"
svm_performance_report = "svm_performance_report"
main_db = 'models/data_set.db'
trigrams_path = 'models/tri_gram.pkl'
input = "models/input.csv"
working_folder = ""

ocr_output_OcropusArgus = "./Evaluation-script/OCROutput/Ocropus/Argus/"
ocr_output_OcropusGrepect = "./Evaluation-script/OCROutput/Ocropus/Grepect/"
ocr_output_TesseractArgus = "./Evaluation-script/OCROutput/Tesseract/Argus/"
ocr_output_TesseractGrepect = "./Evaluation-script/OCROutput/Tesseract/Grepect/"
ocr_output_ABBYYArgus = "./Evaluation-script/OCROutput/ABBYY/Argus/"
ocr_output_ABBYYGrepect = "./Evaluation-script/OCROutput/ABBYY/Grepect/"

output_OcropusArgus = "/output/OcropusArgus/"
output_OcropusGrepect = "/output/OcropusGrepect/"
output_TesseractArgus = "/output/TesseractArgus/"
output_TesseractGrepect = "/output/TesseractGrepect/"
output_ABBYYArgus = "/output/ABBYYArgus/"
output_ABBYYGrepect = "/output/ABBYYGrepect/"

truthArgus = "./Evaluation-script/ManuelTranscript/Argus/"
truthGrepect = "./Evaluation-script/ManuelTranscript/Grepect/"

charReportOcropusArgus = "./Evaluation-script/Reports/CharAcc/Ocropus/Argus/"
charReportOcropusGrepact = "./Evaluation-script/Reports/CharAcc/Ocropus/Grepect/"
charReportTesseractArgus = "./Evaluation-script/Reports/CharAcc/Tesseract/Argus/"
charReportTesseractGrepect = "./Evaluation-script/Reports/CharAcc/Tesseract/Grepect/"
charReportABBYYArgus = "./Evaluation-script/Reports/CharAcc/ABBYY/Argus/"
charReportABBYYGrepect = "./Evaluation-script/Reports/CharAcc/ABBYY/Grepect/"

outputCharReportOcropusArgus = "./Evaluation-script/Reports/CharAcc/Output/Ocropus/Argus/"
outputCharReportOcropusGrepact = "./Evaluation-script/Reports/CharAcc/Output/Ocropus/Grepect/"
outputCharReportTesseractArgus = "./Evaluation-script/Reports/CharAcc/Output/Tesseract/Argus/"
outputCharReportTesseractGrepect = "./Evaluation-script/Reports/CharAcc/Output/Tesseract/Grepect/"
outputCharReportABBYYArgus = "./Evaluation-script/Reports/CharAcc/Output/ABBYY/Argus/"
outputCharReportABBYYGrepect = "./Evaluation-script/Reports/CharAcc/Output/ABBYY/Grepect/"

wordReportOcropusArgus = "./Evaluation-script/Reports/WordAcc/Ocropus/Argus/"
wordReportOcropusGrepact = "./Evaluation-script/Reports/WordAcc/Ocropus/Grepect/"
wordReportTesseractArgus = "./Evaluation-script/Reports/WordAcc/Tesseract/Argus/"
wordReportTesseractGrepect = "./Evaluation-script/Reports/WordAcc/Tesseract/Grepect/"
wordReportABBYYArgus = "./Evaluation-script/Reports/WordAcc/ABBYY/Argus/"
wordReportABBYYGrepect = "./Evaluation-script/Reports/WordAcc/ABBYY/Grepect/"

outputWordReportOcropusArgus = "./Evaluation-script/Reports/WordAcc/Output/Ocropus/Argus/"
outputWordReportOcropusGrepact = "./Evaluation-script/Reports/WordAcc/Output/Ocropus/Grepect/"
outputWordReportTesseractArgus = "./Evaluation-script/Reports/WordAcc/Output/Tesseract/Argus/"
outputWordReportTesseractGrepect = "./Evaluation-script/Reports/WordAcc/Output/Tesseract/Grepect/"
outputWordReportABBYYArgus = "./Evaluation-script/Reports/WordAcc/Output/ABBYY/Argus/"
outputWordReportABBYYGrepect = "./Evaluation-script/Reports/WordAcc/Output/ABBYY/Grepect/"

frontierPath = "./Evaluation-script/ftk-1.0/bin/Linux/"
primaPath = "./Evaluation-script/Prima/PrimaText.jar"
