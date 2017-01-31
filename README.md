# com.castsoftware.uc.imsdc

# IMS/DC and MFS 

# Introduction : 

IMS/DC is an heavy TP transaction monitor. It is not supported by default in AIP (still not supported as of 8.2.0, jan 2017). Here is a custom package aimed to bring minimal support, mostly for transaction identification.

MFS (Message Format Service), MFS is an IMS feature which lets you use Formatted Display Screens. To process a transaction, MFS uses 4 control blocks : DIF (Device Input Format), MOD (Mesg Output Descriptor), MID (Mesg Input Descriptor), DOF (Device Output Format). MFS control statement are often refereed as Format Set (FMT identifies the beginning of a format Set).  

## Roadmap
This custom package is a field-supported package. It has been used in a limited number of situations.


## Source Code Delivery Instructions

The source code for IMS/DC system definition and MFS maps needs to be delivered with the following file extensions ((warning) note these extensions do not exist on the zOS system but have to be added either during the file transfer or after they have been transferred on the Windows system) :
IMS/DC Transaction definition (IMS system definition)
	*.tra	M	
This file lists one or more APPLCTN macros combined with one or more TRANSACT macros.
It defines the scheduling and resource requirements for an application program.
See IBM documentation on how to obtain this file.
This seems to be "stage 1 of IMS system definition" output.

IMS MFS maps definition	*.mfs	O	
See IBM documentation on how to obtain these files (1 file per MFS map).
2 alternative for the source code delivery, when MFS maps are managed in a PDS :
1° Use IEBPTPCH utility as documented at Partitioned Data Set (PDS), and add .mfs extension to all files, Deliver in DMT as Folder on your local file system.
2° Use the Mainframe vendor specific extractor to split a PDS dump (use the Cobol program entry for instance) and rename the .cbl extensions to .mfs.

 ## Additional type of objects bring by this extension 
 
 Objects being part of IMS DC Metamodel : IMS Program, IMS Transaction
 ![IMSDC](/imsdc.jpg)
 
 Objects being part of MFS Metamodel : MID, MOD, FMT
 ![MFS](/mfs.jpg)
 
 
 ## Sample transaction IMSDC end to end graphical view 
 
![Sample transaction IMSDC end to end graphical view](/imsdc_transaction6_PGU_page_Workaround.jpg)



## TCC configuration

According to page Function Points and IMS DC transaction : 
    in case of no MFS (Transaction alone), then IMSDC Transaction should be set as begin of transaction.
    In case of IMSDC Transaction + MFS, then MFS is the begin of transaction.
        Ideally, the FMT should be the entry point since it defines the UI.  If not, you might consider to use the MID (Input message, input to... IMS DC)
	
	
	

