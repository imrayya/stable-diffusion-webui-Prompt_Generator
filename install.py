import launch
if not launch.is_installed("transformers"):
    launch.run_pip("install --upgrade transformers", "Requirement of Prompt-Maker")
if not launch.is_installed("torch"):
    launch.run_pip("install --upgrade torch", "Requirement of Prompt-Maker")