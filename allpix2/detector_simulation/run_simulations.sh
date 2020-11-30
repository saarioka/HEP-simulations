#!/bin/bash

/media/santeri/linux-storage/allpix-squared/build/src/exec/allpix \
    -c thickness_comparison.conf \
    -g dut.sensor_thickness=320um \
    -g dut.sensor_material="Si" \
    -o GenericPropagation.model="Jacoboni" \
    -o root_file="modules_si_320um" \
    -o DetectorHistogrammer.file_name="detector_histogram_si_320um" \
    -o ROOTObjectWriter.file_name="output_si_320um"

/media/santeri/linux-storage/allpix-squared/build/src/exec/allpix \
    -c thickness_comparison.conf \
    -g dut.sensor_thickness=900um \
    -g dut.sensor_material="Si" \
    -o GenericPropagation.model="Jacoboni" \
    -o root_file="modules_si_900um" \
    -o DetectorHistogrammer.file_name="detector_histogram_si_900um" \
    -o ROOTObjectWriter.file_name="output_si_900um"
