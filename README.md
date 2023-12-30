# Three-step-reading
## First pass
Getting title,
abstract,
introduction,
section and subsection,
conclusion, 
reference
## Second pass
Get all paragraph, and figures, diagrams

# Input/Output
+ input : paper parsed json file, and the paper figure path.
+ output : sections of the paper
# Attention
+ Alter the `DISPLAY_MODE` to `True` to see the run result.
+ Specify the image output dir by setting `output_dir` 
# Problem existing
+ In `CONCLUSION` part, Conclusion and Acknowledgments are in the same json object. 
+ Diagram with no corresponding name