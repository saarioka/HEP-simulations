#!/bin/bash

allpix -c thickness_comparison.conf -g dut.sensor_thickness=320um -o root_file=modules_320um -o DetectorHistogrammer.file_name="detector_histogram_320um" -o ROOTObjectWriter.file_name="output_320um" -v DEBUG
allpix -c thickness_comparison.conf -g dut.sensor_thickness=900um -o root_file=modules_900um -o DetectorHistogrammer.file_name="detector_histogram_900um" -o ROOTObjectWriter.file_name="output_900um" -v DEBUG
