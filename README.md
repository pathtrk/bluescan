# BlueScan - Azure OCR library

## Install

```bash
pip install -e .
```

## Usage

First set Azure endpoint and API key to environmetal variables

```powershel
$Env:AZURE_CV_URL=<your_Azure_computer_vision_API_endpoint>
$Env:AZURE_CV_KEY=<your_Azure_computer_vision_API_key>
```

Or on \*nix,

```bash
export AZURE_CV_URL=<your_Azure_computer_vision_API_endpoint>
export ZURE_CV_KEY=<your_Azure_computer_vision_API_key>
```

To run:

```bash
python -m bluescan.azure <path_to_local_image>
```

## Notice

Azure Computer Vision has an image size limit for its free/trial plan. Beware size of your uploading image.
