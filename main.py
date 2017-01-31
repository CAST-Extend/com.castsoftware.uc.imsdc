import cast_upgrades.application_1_4_5 # @UnusedImport

from cast.application import ApplicationLevelExtension, ReferenceFinder, create_link
from cast.analysers import log
import logging

class MyIMSDCExtension(ApplicationLevelExtension):

    def __init__(self):   
        pass     
        
    def end_application(self, application):

        self.links_from_IMS_Programs_to_PSB(application)
        self.links_from_IMS_Program_to_Cobol_Program(application)
        self.links_from_IMS_Transactions_to_IMS_Programs(application)
        self.links_from_MFS_MID_to_IMS_Transactions(application)
        self.link_between_the_PSB_used_in_transactional_mode_and_his_PCBs(application)

    def links_from_IMS_Programs_to_PSB(self, application): 
        
        nb_links = 0 
        logging.info("==> solves the following problem : Missing links between IMS Programs and PSB")    

        # 1. search all references in all files
 
        logging.info("Scanning IMS files for calls to IMS PSB")
 
        ims_psbs = {} 
            
        for ims_psb in application.search_objects(category='CAST_IMS_ProgramSpecificationBlock'):
            ims_psbs[ims_psb.get_name()] = ims_psb    
 
        # 2. scan each program
        # we search a pattern
        cobol_and_psb_access = ReferenceFinder()
        cobol_and_psb_access.add_pattern("psb", before="", element="PSB=([a-zA-Z_0-9.#\(\)\:\&\; ]*)", after="")
 
        links = []
                 
        for o in application.get_files(['sourceFile']):
             
            # check if file is analyzed source code, or if it generated (Unknown)
            if not o.get_path():
                continue
            
            if not o.get_path().lower().endswith('.tra'):
                continue
            
            for reference in cobol_and_psb_access.find_references_in_file(o):
                    
                #logging.debug("Reference " + reference.value)      
                
                # manipulate the reference pattern found
                searched_psb_name = reference.value.split("=")[1]
 
                #logging.debug("searching " + searched_psb_name)
 
                try:
                    ims_psb = ims_psbs[searched_psb_name]
                    links.append(('callLink', reference.object, ims_psb, reference.bookmark))
                    
                except:
                    pass
         
        # 3. Create the links
        for link in links:
            logging.debug("Creating link between " + str(link[1]) + " and " + str(link[2]))
            create_link(*link)
            nb_links = nb_links + 1 
                
        logging.debug("Nb of links created " + str(nb_links))             
 
    def links_from_IMS_Program_to_Cobol_Program(self, application): 
        
        nb_links = 0 
        logging.info("==> solves the following problem : Missing links between IMS Program and Cobol Program")    

        # 1. search all references in all files
 
        logging.info("Scanning IMS files for calls to Cobol Programs")
 
        cobol_programs = {}
         
        for cobol_program in application.search_objects(category='CAST_COBOL_Program'):
            cobol_programs[cobol_program.get_name()] = cobol_program 
 
        # 2. scan each program
        # we search a pattern
        cobol_and_psb_access = ReferenceFinder()
        cobol_and_psb_access.add_pattern("cobol", before="", element="PSB=([a-zA-Z_0-9.#\(\)\:\&\; ]*)", after="")
 
        links = []
                 
        for o in application.get_files(['sourceFile']):
             
            # check if file is analyzed source code, or if it generated (Unknown)
            if not o.get_path():
                continue
            
            if not o.get_path().lower().endswith('.tra'):
                continue
             
            for reference in cobol_and_psb_access.find_references_in_file(o):
                    
                #logging.debug("Reference " + reference.value)      
                
                # manipulate the reference pattern found
                searched_cobol_name = reference.value.split("=")[1]
 
                #logging.debug("searching " + searched_cobol_name)
 
                try:
                    cobol_program = cobol_programs[searched_cobol_name]
                    links.append(('callLink', reference.object, cobol_program, reference.bookmark))
                    
                except:
                    pass
         
        # 3. Create the links
        for link in links:
            logging.debug("Creating link between " + str(link[1]) + " and " + str(link[2]))
            create_link(*link)
            nb_links = nb_links + 1 
                
        logging.debug("Nb of links created " + str(nb_links))     
    
    def links_from_IMS_Transactions_to_IMS_Programs(self, application): 
        
        logging.info("==> solves the following problem :  create links from IMS Transactions to IMS Programs ")    

        application.update_cast_knowledge_base("links_from_IMS_Transactions_to_IMS_Programs", """     
        insert into ci_links(caller_id, called_id, link_type, error_id)
        select tx.object_id, prg.object_id, 'callLink', 0
        from ctv_guid_objects tx
        inner join ctv_guid_parents txprg
        on txprg.object_id = tx.object_id
        inner join ctv_guid_objects prg
        on prg.object_id = txprg.parent_id
        inner join ctt_object_applications prgapp
        on prgapp.object_id = prg.object_id
        inner join csv_ana_appli appana
        on appana.application_id = prgapp.application_id
        where tx.object_type_str = 'IMS Transaction'
        and prg.object_type_str = 'IMS Program'
        and prgapp.application_type = 1000001
        """) 
    
    def links_from_MFS_MID_to_IMS_Transactions(self, application): 
        
        nb_links = 0 
        logging.info("==> solves the following problem : MFS MID to IMS Transactions")    

        # 1. search all references in all files
        logging.info("Scanning MFS files for calls to IMS Transactions")
        
        mfs_mids = {} 
            
        for mfs_mid in application.search_objects(category='MFS-MID'):
            mfs_mids[mfs_mid.get_name()] = mfs_mid   
 
        ims_transactions = {} 
            
        for ims_transaction in application.search_objects(category='IMSDCTransaction'):
            ims_transactions[ims_transaction.get_name()] = ims_transaction    
 
            
 
        # 2. scan each program
        # we search a pattern
        ims_access = ReferenceFinder()
        #ims_access.add_pattern("Begin_IMS_Transaction", before="", element="MSG[ ]+TYPE", after="")
        ims_access.add_pattern("Begin_IMS_Transaction", before="", element="[A-Z0-9]+[ ]+MSG[ ]+TYPE", after="")
        #YFP21I   MSG   TYPE=INPUT
        ims_access.add_pattern("Expression_IMS_Transaction", before="", element="MFLD[ ]+'([^']+)", after="")
        ims_access.add_pattern("End_IMS_Transaction", before="", element="MSGEND", after="")

        links = []
        inside = False
                 
        for o in application.get_files(['sourceFile']):
             
            # check if file is analyzed source code, or if it generated (Unknown)
            if not o.get_path():
                continue
            
            if not o.get_path().lower().endswith('.mfs'):
                continue
            
            #logging.debug("file = " + o.get_path())
            
            for reference in ims_access.find_references_in_file(o):
                    
                #logging.debug("Reference " + reference.value)      
                
                if reference.pattern_name == "Begin_IMS_Transaction": 
                    searched_mfs_mid = reference.value.split(" ")[0]
                    #logging.debug("searching mfs mid " + searched_mfs_mid)
                    inside = True 
                
                if reference.pattern_name == "End_IMS_Transaction": 
                    inside = False  
                    
                if (reference.pattern_name == "Expression_IMS_Transaction") and (inside == True): 
   
                    # manipulate the reference pattern found
                    searched_ims_transaction_name = reference.value.split("'")[1]
                    if searched_ims_transaction_name.strip(): # exclude the empty strings 
         
                        #logging.debug("searching " + searched_ims_transaction_name)
         
                        try:
                            ims_transaction = ims_transactions[searched_ims_transaction_name]
                            mfs_mid = mfs_mids[searched_mfs_mid]
                            links.append(('callLink', mfs_mid, ims_transaction, reference.bookmark))
                                
                        except:
                            pass
         
        # 3. Create the links
        for link in links:
            logging.debug("Creating link between " + str(link[1]) + " and " + str(link[2]))
            create_link(*link)
            nb_links = nb_links + 1 
                
        logging.debug("Nb of links created " + str(nb_links))             
 
                
    def link_between_the_PSB_used_in_transactional_mode_and_his_PCBs(self, application): 
        
        logging.info("==> solves the following problem :  Create link between the PSB used in transactional mode and his PCBs. The resolution of the PSB is only available if your pcb will be referenced by a JCL so in batch mode. Most of the time these PGM will use a PSB with the same name. This is not all the time the case but the script below address at least this case. The links to the PCB are only created if you have a match between program and PSB ")    

        application.update_cast_knowledge_base("link_between_the_PSB_used_in_transactional_mode_and_his_PCBs", 
        """         
        INSERT into CI_LINKS (CALLER_ID, CALLED_ID, LINK_TYPE, ERROR_ID)
            SELECT caller.object_id,called.object_id, 'callLink', 0
            FROM    cdt_objects caller,
            ctt_object_parents par,
            cdt_objects called
            WHERE caller.object_type_str ='IMS PSB'
            AND caller.object_fullname not like '[Unknown%'
            AND par.parent_id = caller.object_id
            AND called.object_id = par.object_id
            AND caller.object_name in (
            SELECT object_name
            FROM cdt_objects
            WHERE object_type_str ='Cobol Program'
            AND object_name in (select object_name
            FROM cdt_objects
            WHERE object_type_str ='IMS PSB'
            AND object_fullname not like '[Unknown%' )
            )
            order by caller.object_name,called.object_name
        """)  
        


    

            
