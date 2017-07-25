# trustar-splinter
This tool ingests malware configuration settings and indicators of compromise (IOCs) to predict the RAT malware family most likely associated with the user provided IOCs. The predictions are presented as a collection of probability assignments to different RAT malware families. 

## Setup

In order to use `splinter`, you need to make sure you are running `python 2.7.x` and have `pip` installed. 

1. Start by cloning the repository. 
2. Run `pip install -r requirements.txt` to make sure you have all dependancies installed. 
3. Try running `cd src & python splinter.py test`. If this does not raise any exceptions, you are ready to move on. 

## Using Splinter

There are two ways to use splinter out of the box. 


1. Provide IOCs as command line arguments. An example of this call is 
              
        python splinter.py IOC1 IOC2 IOC3 IOC4
        
    The model will use the four IOCS: IOC1, IOC2, IOC3, and IOC4 to make a 
    prediction about which RAT the IOCs are connected to.

2. Provide a list of IOCs in a text file separated by commas, or new lines. An example of this call, 
with a file named `iocfile.txt`, is

        python splinter.py iocfile.txt

    The model extracts the IOCs in `iocfile.txt` and uses them to make a 
    prediction about which RAT the IOCs are connected to.
