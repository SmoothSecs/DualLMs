# DualLM

**DualLM** is an open-source tool for detecting security-critical Linux kernel patches, focusing on **use-after-free (UAF)** and **out-of-bounds (OOB)** vulnerabilities. It uses a dual-model pipeline combining a **Large Language Model (LLM)** and a **fine-tuned lightweight model** to analyze commit messages and code diffs with high accuracy.

📌 **Highlights**:
- 87.4% accuracy, 0.875 F1-score  
- Outperforms SID and TreeVul  
- Identified 90+ verified UAF/OOB patches (incl. silent fixes)  
- Includes PoCs for confirmed vulnerabilities  

DualLM helps downstream maintainers and security teams prioritize critical patches faster and more reliably.

# Setup

## Hardware Requirements

- Ubuntu Desktop (recommended: Ubuntu 24.04 LTS)
- NVIDIA GPU with CUDA support
- Minimum 16GB RAM recommended


## Environment
We use conda to manage the running environemnt, please see https://anaconda.org/anaconda/conda for details to install conda.

## Dependencies

DualLM relies on Joern(https://github.com/joernio/joern) for the slicing.  A jern.zip has been uploaded to the root folder of DualLMs. please unzip it and keep it under DualLMs root.

## Models

The models are stored under PROJECT_FOLDER/models.  just download them and keep them there.

## API Keys

DualLM requires an OpenAI API key to function. To set up your API key: edit step1.sh.
```
#export OPENAI_API_KEY="your-openai-api-key-here"
```

## Linux Repo.
clone Linux repo into ./repos/. so the system can fetch the commits information from repo.

## Input & Output
   The input is a list of commits, output is the evaluation of those commits, are they security related patches, etc.

##  Step 1: run the analysis using LLM.

### Setup Environment
```conda create --name dualLMStep1 python=3.10
   conda activate dualLMStep1
```
### install the depedencies
```
pip3 install -r requirements.txt
```
### run the script.
```
./step1.sh
```
### Output

"reliable" commits are commits that contain enough information to determine if this commit is a security patch and its type.  "Non-reliable" means 


## step 2: run the analysis on on-reliable commits.

### Setup Environment
```
conda create --name dualLMStep2 python=3.6.10
conda activate dualLMStep2
onda config --add channels conda-forge
conda config --add channels pytorch

conda install pytorch==1.5.1 torchvision==0.6.1 cudatoolkit=10.2 -c pytorch
conda install submitit sklearn

```
### install dependencies 
```
pip3 install -r requirements2.txt
```

### there are two steps.
```
cd codes
./eval_given_step1.sh
./eval_given_step2.sh
```

## Results.
Under folder data/results, you can see the analyzed resutls.

{'9d7a0577c9db35c4cc52db90bc415ea248446472': ["Analysis:\nThe commit title and message largely discuss issues related to compiler warnings in GCC and the handling of certain types of string initialization warning (`-Wunterminated-string-initialization`). The content appears to focus on compiler flags adjustments specifically for addressing these warnings that the developer found either too verbose or erroneous. It does not mention or indicate concerns directly related to the specific runtime execution or memory manipulation bugs that would correspond to use-after-free, memory out-of-bounds, null pointer dereference, memory leak, or use-before-initialization.\n\nIn the diff provided:\n- The Makefile amendment is about disabling a specific warning (`-Wunterminated-string-initialization`), altering the compile-time flags. \n- In `drivers/acpi/tables.c`, the change removes the `__nonstring` attribute from `table_sigs`. This attribute is used to tell the compiler that the data should not be treated as a string, addressing a type interpretative issue at compilation, not directly affecting memory or execution safety at runtime concerning the bug types we're discussing (use-after-free, memory out-of-bounds, null pointer dereference, etc.).\n\nThe patch, while adjusting how the compiler should treat certain constructs (e.g., string arrays in the context of warnings), does not address any of the typical behaviors associated with the stated bug types. For instance, there are no adjustments to memory allocation, no additional checks against null pointers, and no changes in memory access patterns that would suggest preventing use-after-free, buffers overbounds, or similar runtime issues.\n\nContains reliable hints about the bug type: no; the description and changes mainly focus on compiler behavior rather than runtime memory bugs or operational errors.", '```json\n{\n  "contain reliable hints":"no"\n}\n```'], '79dc7e3f1cd3': ['Analysis:\n\n1. Commit Title and Message: The title suggests a fix involving handling cases where there is no destination entry (`dst`) on a socket buffer (`skb`) in an `icmp6_send` function. The commit message elaborates on a bug encountered during kernel fuzzing with syzkaller concerning possible null-pointer dereferences. This could imply that the bug type is related to null pointer dereference since a general protection fault was mentioned, commonly associated with null pointer dereferences or similar memory access violations.\n\n2. Commit Diff:\n```diff\n-\tiif = l3mdev_master_ifindex(skb_dst(skb)->dev);\n+\tdst = skb_dst(skb);\n+\tiif = l3mdev_master_ifindex(dst ? dst->dev : skb->dev);\n```\nThe diff modifies the handling inside `icmp6_send` to add a check on `skb_dst(skb)`, storing the result in the local `dst` variable before using it. The code now checks whether `dst` is not null before accessing `dst->dev`, and if `dst` is null, it falls back to using `skb->dev`.\n\nThis additional null check and conditional access of `dst->dev` align with the common pattern of adding checks to verify pointers are not null before dereferencing them, aiming to prevent null pointer dereferences.\n\nContains reliable hints about the bug type: yes; the bug type is non-uaf-oob (null pointer dereference). This is inferred from the explicit handling introduced in the code for potential null values of `dst`, matching the scenario described in the commit message about potential null-pointer deref issues observed during fuzz testing.', '```json\n{\n  "contain reliable hints": "yes",\n  "bug type": "null pointer dereference"\n}\n```']}
