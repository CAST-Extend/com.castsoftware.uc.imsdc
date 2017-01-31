# com.castsoftware.uc.imsdc

# IMS/DC and MFS Analyzers 

# Introduction : 

IMS/DC is an heavy TP transaction monitor. It is not supported by default in AIP (still not supported as of 8.2.0, jan 2017). Here is a custom package aimed to bring minimal support, mostly for transaction identification.

MFS (Message Format Service), MFS is an IMS feature which lets you use Formatted Display Screens. To process a transaction, MFS uses 4 control blocks : DIF (Device Input Format), MOD (Mesg Output Descriptor), MID (Mesg Input Descriptor), DOF (Device Output Format). MFS control statement are often refereed as Format Set (FMT identifies the beginning of a format Set).  

## Roadmap
This custom package is a field-supported package. It has been used in a limited number of situations.
This package is initially based on UA, reference finders, and KB Update. 
This package has been tested in CAST 8.0.x 

TODO : add a discoverer 

## Source Code Delivery Instructions
The source code for IMS/DC system definition and MFS maps needs to be delivered with the following file extensions ((warning) note these extensions do not exist on the zOS system but have to be added either during the file transfer or after they have been transferred on the Windows system) :

| Source code type | Required file extensions | Mandatory / Optional | Comments                                         | 
|------------------|:------------------------:|:--------------------:|------------------------------------------------:|
|IMS/DC Transaction definition (IMS system definition)  | tra | M | This file lists one or more APPLCTN macros combined with one or more TRANSACT macros. It defines the scheduling and resource requirements for an application program. See IBM documentation on how to obtain this file. This seems to be "stage 1 of IMS system definition" output. | 
| IMS MFS maps definition | mfs | O | See IBM documentation on how to obtain these files (1 file per MFS map). 2 alternative for the source code delivery, when MFS maps are managed in a PDS : (1) Use IEBPTPCH utility as documented at Partitioned Data Set (PDS), and add .mfs extension to all files, Deliver in DMT as Folder on your local file system. (2) Use the Mainframe vendor specific extractor to split a PDS dump (use the Cobol program entry for instance) and rename the .cbl extensions to .mfs. | 

TRA file sample 1 : 
```
         APPLCTN PSB=ANT001,PGMTYPE=TP,SCHDTYP=PARALLEL                 00001400
         TRANSACT CODE=ANTPSR,MSGTYPE=(MULTSEG,RESPONSE,4),            *00001500
               PARLIM=0,SEGNO=400,                                     *00001600
               MODE=SNGL,PROCLIM=(03,01)                                00001700
...
         APPLCTN PSB=ANT100,PGMTYPE=BATCH                               00001800
         TRANSACT CODE=ANT100,MSGTYPE=(MULTSEG,NONRESPONSE,6),         *00001900
               MODE=SNGL,PRTY=(0,0),PROCLIM=(03,01)                     00002000

```

TRA file sample 2 : 
```
  APPLCTN PSB=ABPG625,PGMTYPE=(TP),FPATH=NO,SCHDTYP=PARALLEL
            TRANSACT CODE=625AB,                                       +
               PRTY=(1,1,65535),                                       +
               MSGTYPE=(SNGLSEG,RESPONSE,1),PROCLIM=(5,2),             +
               PARLIM=3,SCHD=1,INQUIRY=(NO,RECOVER),MAXRGN=2,          +
               MODE=SNGL,EDIT=(UC),FPATH=NO,SEGNO=1000,                +
               DCLWA=YES,AOI=NO  
...
 APPLCTN PSB=AGPGA11,PGMTYPE=(BATCH),FPATH=NO,                 +
               SCHDTYP=PARALLEL
...
 APPLCTN GPSB=ABLK406,LANG=ASSEM,PGMTYPE=(BATCH),FPATH=NO,     +
               SCHDTYP=PARALLEL
 APPLCTN GPSB=AHHSA,LANG=COBOL,PGMTYPE=(TP),FPATH=NO,          +
               SCHDTYP=PARALLEL
```

## Additional type of objects bring by this extension 
Objects being part of IMS DC Metamodel : IMS Program, IMS Transaction 

![IMSDC](/imsdc.jpg)
Objects being part of MFS Metamodel : MID, MOD, FMT 


![MFS](/mfs.jpg) 

## Cases covered by this extension 

The following cases are covered by the extension : 
- creation of objects for IMS/DC programs / transactions and MFS screens  
- creation of links from IMS Programs to PSB's
- creation of links from IMS Program to Cobol Program
- creation of links from IMS Transactions to IMS Programs
- creation of links from MFS MID's to IMS Transactions 
- creation of links between the PSB used in transactional mode and his PCBs.  

## Sample transactions IMSDC end to end graphical view 
![Sample transaction IMSDC end to end graphical view](/imsdc_transaction6_PGU_page_Workaround.jpg)

![Sample2 transaction IMSDC end to end graphical view](/imsdc transaction with comments.jpg)

## TCC configuration
- in case of no MFS (Transaction alone), then IMSDC Transaction should be set as begin of transaction.
- in case of IMSDC Transaction + MFS, then MFS is the begin of transaction.
        Ideally, the FMT should be the entry point since it defines the UI.  If not, you might consider to use the MID (Input message, input to... IMS DC)
	
