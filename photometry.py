import datajoint as dj
import matplotlib.pyplot as plt

dj.config['database.host'] = '127.0.0.1'
dj.config['database.user'] = 'root'
dj.config['database.password'] = 'tut'

dj.conn()

schema = dj.schema('photometry', locals())

schema.drop()

@schema
class AnimalID(dj.Manual):
    definition = """
    animal_id: int # unique mouse identifier
    """

@schema
class AnimalInactive(dj.Manual):
    definition = """
    -> AnimalID
    """

@schema
class AnimalDetails(dj.Manual):
    definition = """
    -> AnimalID
    ---
    genotype: varchar(32)
    source: varchar(32)
    sex: varchar(1)
    dob: date # date of birth
    
    #surgery_info
    #exp_class: varchar(32)
    """

@schema
class FiberID(dj.Manual):
    definition = """
    -> AnimalID
    fiber_id: int
    """
    

@schema
class FiberSurgery(dj.Manual):
    definition = """
    -> FiberID
    ---
    fiber_name: varchar(32)
    implant_type: varchar(32)
    implant_site: varchar(32)
    
    virus: varchar(32)
    volume: float
    titer: varchar(32)
    injection_site: varchar(32)
    injection_date: date
    implant_date: date
    """

@schema
class SessionID(dj.Manual):
    definition = """
    -> AnimalID
    session_id: smallint
    """

@schema
class SessionInactive(dj.Manual):
    definition = """
    -> SessionID
    """

@schema
class SessionDetails(dj.Manual):
    definition = """
    -> SessionID
    ---
    sesion_date: date
    session_time: time
    behavioral_conditions: varchar(256)
    neural_conditions: varchar(256)
    rec_technique = "photometry": varchar(32) # 'photometry'
    experiment_type: varchar(32) # 'headfixed' or 'freelymoving'
    session_note = "": varchar(256)
    
    #session_directory = "": varchar(256)
    #-> ExperimentType
    #-> RecordingTechnique
    """

@schema
class BehavioralTimeSeries(dj.Manual):
    definition = """
    -> SessionID
    ---
    behavioral_data: longblob
    """
    
    class TrialAligned(dj.Part):
        definition = """
        -> master
        ---
        aligned_behavioral_data: longblob
        """

@schema
class BehavioralEvents(dj.Manual):
    definition = """
    -> BehavioralTimeSeries.TrialAligned
    ---
    behavioral_events: longblob
    """
    
@schema
class PhotometryTimeSeries(dj.Manual):
    definition = """
    -> SessionID
    -> FiberSurgery
    ---
    photometry_data: longblob
    """

@schema
class TrialAlignedTimeSeries(dj.Manual):
    definition = """
    -> BehavioralTimeSeries.TrialAligned
    -> PhotometryTimeSeries
    ---
    aligned_behavioral_data: longblob
    aligned_phtometry_data: longblob
    """

plt.figure(figsize=(30,20))
dj.ERD(schema).draw()