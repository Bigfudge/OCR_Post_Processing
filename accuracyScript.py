import os
import constants as c
import combined_accuracy_dir as comb


def combined_accuracy_report():
    comb.combined_accuracy_dir(c.output_OcropusArgus, c.truthArgus, "Argus",
                               os.path.join(c.working_folder, "AccuracyReportOcropusArgus.txt"))
    comb.combined_accuracy_dir(c.output_OcropusGrepect, c.truthGrepect, "Grepect",
                               os.path.join(c.working_folder, "AccuracyReportOcropusArgus.txt"))
    comb.combined_accuracy_dir(c.output_TesseractArgus, c.truthArgus, "Argus",
                               os.path.join(c.working_folder, "AccuracyReportTesseractArgus.txt"))
    comb.combined_accuracy_dir(c.output_TesseractGrepect, c.truthGrepect, "Grepect",
                               os.path.join(c.working_folder, "AccuracyReportTesseractGepect.txt"))
    comb.combined_accuracy_dir(c.output_ABBYYArgus, c.truthArgus, "Argus",
                               os.path.join(c.working_folder, "AccuracyReportABBYYArgus.txt"))
    comb.combined_accuracy_dir(c.output_ABBYYGrepect, c.truthGrepect, "Grepect",
                               os.path.join(c.working_folder, "AccuracyReportABBYYGrepect.txt"))


combined_accuracy_report()
