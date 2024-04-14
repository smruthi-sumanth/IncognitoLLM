from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class Complainant(BaseModel):
    name: str = Field(title="Name")
    f_or_h_name: str = Field(title="Father's or Husband's Name")
    email: str = Field(title="Email")
    phone: int = Field(title="Phone Number")
    address: str = Field(title="Address")
    age: int = Field(title="Age")
    occupation: str = Field(title="Labourer")
    religion: str = Field(title="Religion")
    caste: str = Field(title="Caste")
    passport_no: str = Field(title="Passport Number")
    aadhar_no: str = Field(title="Aadhar Number")
    nationality: str = Field(title="Nationalality")
    sex: str = Field(title="Gender")


class Header(BaseModel):
    fIRNo: str = Field(title="Crime Number")
    sub_division: str = Field(title="Circle/Sub Division")
    district: str = Field(title="District")
    fir_date: str = Field(title="FIR Date")
    unitName: str = Field(title="Police Station Name")

class Occurrence(BaseModel):
    day: str = Field(title="Day of Occurrence of Offence")
    from_date: str = Field(title="From Date of Occurrence")
    to_date: str = Field(title="To Date of Occurrence")
    from_time: str = Field(title="From Time of Occurrence")
    to_time: str = Field(title="To Time of Occurrence")
    info: str = Field(title="Information received at the PS")
    district: str = Field(title="District")
    w_or_o: str = Field(title="Written or Oral")
    delay_reason: str = Field(title="Reason for Delay in reporting by the Complainant/Informant")
    general_diary_no: str = Field(title="General Diary Number")
    place_of_occurrence: str = Field(title="Place of Occurrence with full address")
    distance: str = Field(title="Distance from PS")
    village: str = Field(title="Village")
    beat: str = Field(title="Beat Name")

class Suspect(BaseModel):
    idx: int = Field(title="Sl. No.")
    identifier: str = Field(title="Name or Father's Name or Caste or Address")
    type: str = Field(title="Type of Suspect")
    person_type: str = Field(title="Person Type")
    sex: str = Field(title="Gender")
    age: int = Field(title="Age")
    occupation: str = Field(title="Labourer")

class Victim(BaseModel):
    idx: int = Field(title="Sl. No.")
    name: str = Field(title="Name")
    injury_type: str = Field(title="Type of Injury")
    sex: str = Field("Gender")
    age: int = Field("Age")
    occupation: str = Field("Occupation")

class StolenProperty(BaseModel):
    idx: int = Field(title="Sl. No.")
    property_type: str = Field(title="Type of Property")
    value: str = Field(title="Estimated Value of Property")
    description: str = Field(title="Item Description")


class FIRDetails(BaseModel):
    district: Optional[str] = Field(title="District")
    crime_no: Optional[str] = Field(title="Crime No")
    fir_date: Optional[str] = Field(title="FIR Date")
    circle_sub_division: Optional[str] = Field(title="Circle/Sub Division")
    police_station: Optional[str] = Field(title="PS")
    act_section: Optional[str] = Field(title="Act & Section")
    information_received_at_ps: Optional[str] = Field(title="Information received at the PS")
    information_received_type: Optional[str] = Field(title="Written/Oral")
    information_received_from_time: Optional[str] = Field(title="From Time")
    information_received_to_time: Optional[str] = Field(title="To Time")
    information_received_from_date: Optional[str] = Field(title="From Date")
    information_received_to_date: Optional[str] = Field(title="To Date")
    occurrence_of_offence_day: Optional[str] = Field(title="Occurrence of Offence Day")
    general_diary_reference_entry_no: Optional[int] = Field(title="General Diary reference Entry No.")
    general_diary_reference_time: Optional[str] = Field(title="General Diary reference Time")
    place_of_occurrence_address: Optional[str] = Field(title="Place of occurrence with full address")
    place_of_occurrence_distance_from_ps: Optional[str] = Field(title="Distance from PS")
    place_of_occurrence_village: Optional[str] = Field(title="Village")
    place_of_occurrence_beat_name: Optional[str] = Field(title="Beat Name")
    place_of_occurrence_district: Optional[str] = Field(title="District")
    complainant_informant_name: Optional[str] = Field(title="Name")
    complainant_informant_father_husband_name: Optional[str] = Field(title="Father's/Husband's Name")
    complainant_informant_age: Optional[str] = Field(title="Age")
    complainant_informant_occupation: Optional[str] = Field(title="Occupation")
    complainant_informant_religion: Optional[str] = Field(title="Religion")
    complainant_informant_caste: Optional[str] = Field(title="Caste")
    complainant_informant_phone_no: Optional[str] = Field(title="Phone No.")
    complainant_informant_nationality: Optional[str] = Field(title="Nationality")
    complainant_informant_passport_no: Optional[str] = Field(title="Passport No.")
    complainant_informant_passport_date_of_issue: Optional[str] = Field(title="Date of Issue")
    complainant_informant_address: Optional[str] = Field(title="Address")
    complainant_informant_sex: Optional[str] = Field(title="Sex")
    complainant_informant_seen_occurrence: Optional[str] = Field(title="Whether complainant has seen the occurence or merely heard of it",)
    accused_details: Optional[List[dict]] = Field(title="Details of known/suspected/unknown accused with full particulars")
    victim_details: Optional[List[dict]] = Field(title="Details of Victims with full particulars")
    stolen_property_details: Optional[List[dict]] = Field(title="Particulars of Property stolen/involved with value")
    inquest_report_ud_case_no: Optional[str] = Field(title="Inquest Report/U.D. Case No. if any")
    fir_contents: Optional[str] = Field(title="F.I.R Contents")
    action_taken: Optional[str] = Field(title="Action Taken"),
    fir_dispatch_date_time: Optional[str] = Field(title="Date and time of dispatch to the Court")
    fir_carrier_name: Optional[str] = Field(title="Name of PC/HC who carried the FIR to the Court")


