import os
from pathlib import Path
from urllib.parse import quote_plus
from typing import Optional
from pydantic import BaseModel, Field
PROJECT_ROOT = Path(__file__).parent.parent
from dotenv import load_dotenv
load_dotenv()

SHAPEFILES_DIR = PROJECT_ROOT / "shapefiles"

SSL_CERT_PATH = PROJECT_ROOT / "certs" / "ca-certificate.crt"

# Database connection details
DB_USER = os.environ.get('DB_USER')
DB_PASS = quote_plus(os.environ.get('DB_PASS'))
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')



ANALYZER_INFERENCE_URL = "https://p1utoze--presidio-analyzers-flairanalyzer-flair-text-analyzer.modal.run"

_page_config = dict(
        page_title="SecurA",
        page_icon="👮🏻",
        layout="wide",
    )

FLAIR_ENTITIES = [
    "IN_AADHAAR",
    "IN_PAN",
    "US_PASSPORT",
    "US_BANK_NUMBER",
    "IBAN_CODE",
    "CRYPTO",
    "EMAIL_ADDRESS",
    "ADDRESS",
    "AGE",
    "NAME",
    "CREDIT_CARD",
    "DATE_TIME",
    "PERSON",
    "PHONE_NUMBER",
    "ORGANIZATION",
    "IN_VEHICLE_REGISTRATION",
    "LOCATION",
    "GENERIC_PII",
    "ID"
]

COMPLAINT_DICT  = {
    "complainant_informant_name": "Name",
    "complainant_informant_father_husband_name": "Father's/Husband's Name",
    "complainant_informant_age": "Age",
    "complainant_informant_occupation": "Occupation",
    "complainant_informant_religion": "Religion",
    "complainant_informant_caste": "Caste",
    "complainant_informant_phone_no": "Phone No.",
    "complainant_informant_nationality": "Nationality",
    "complainant_informant_passport_no": "Passport No.",
    "complainant_informant_passport_date_of_issue": "Date of Issue",
    "complainant_informant_address": "Address",
    "complainant_informant_sex": "Sex",
    "complainant_informant_seen_occurrence": "Whether complainant has seen the occurence or merely heard of it"
}

class FIRDetails(BaseModel):
    district: Optional[str] = Field(title="District", json_schema_extra={"is_anonymized": True, "section": 1})
    crime_no: Optional[str] = Field(title="Crime No", json_schema_extra={"is_anonymized": True, "section": 1})
    fir_date: Optional[str] = Field(title="FIR Date", json_schema_extra={"is_anonymized": True, "section": 1})
    circle_sub_division: Optional[str] = Field(title="Circle/Sub Division", json_schema_extra={"is_anonymized": True, "section": 1})
    police_station: Optional[str] = Field(title="PS", json_schema_extra={"is_anonymized": True, "section": 1})
    act_section: Optional[str] = Field(title="Act & Section", json_schema_extra={"is_anonymized": True, "section": 2})
    information_received_at_ps: Optional[str] = Field(title="Information received at the PS", json_schema_extra={"is_anonymized": True, "section": 3})
    information_received_type: Optional[str] = Field(title="Written/Oral", json_schema_extra={"is_anonymized": True, "section": 3})
    information_received_from_time: Optional[str] = Field(title="From Time", json_schema_extra={"is_anonymized": True, "section": 3})
    information_received_to_time: Optional[str] = Field(title="To Time", json_schema_extra={"is_anonymized": True, "section": 3})
    information_received_from_date: Optional[str] = Field(title="From Date", json_schema_extra={"is_anonymized": True, "section": 3})
    information_received_to_date: Optional[str] = Field(title="To Date", json_schema_extra={"is_anonymized": True, "section": 3})
    occurrence_of_offence_day: Optional[str] = Field(title="Occurence of Offence Day", json_schema_extra={"is_anonymized": True, "section": 3})
    general_diary_reference_entry_no: Optional[int] = Field(title="General Diary reference Entry No.", json_schema_extra={"is_anonymized": True, "section": 3})
    general_diary_reference_time: Optional[str] = Field(title="General Diary reference Time", json_schema_extra={"is_anonymized": True, "section": 3})
    place_of_occurrence_address: Optional[str] = Field(title="Place of occurence with full address", json_schema_extra={"is_anonymized": True, "section": 4})
    place_of_occurrence_distance_from_ps: Optional[str] = Field(title="Distance from PS", json_schema_extra={"is_anonymized": True, "section": 4})
    place_of_occurrence_village: Optional[str] = Field(title="Village", json_schema_extra={"is_anonymized": True, "section": 4})
    place_of_occurrence_beat_name: Optional[str] = Field(title="Beat Name", json_schema_extra={"is_anonymized": True, "section": 4})
    place_of_occurrence_district: Optional[str] = Field(title="District", json_schema_extra={"is_anonymized": True, "section": 4})
    complainant_informant_name: Optional[str] = Field(title="Name", json_schema_extra={"is_anonymized": True, "section": 5})
    complainant_informant_father_husband_name: Optional[str] = Field(title="Father's/Husband's Name", json_schema_extra={"is_anonymized": True, "section": 5})
    complainant_informant_age: Optional[int] = Field(title="Age", json_schema_extra={"is_anonymized": True, "section": 5})
    complainant_informant_occupation: Optional[str] = Field(title="Occupation", json_schema_extra={"is_anonymized": True, "section": 5})
    complainant_informant_religion: Optional[str] = Field(title="Religion", json_schema_extra={"is_anonymized": True, "section": 5})
    complainant_informant_caste: Optional[str] = Field(title="Caste", json_schema_extra={"is_anonymized": True, "section": 5})
    complainant_informant_phone_no: Optional[str] = Field(title="Phone No.", json_schema_extra={"is_anonymized": True, "section": 5})
    complainant_informant_nationality: Optional[str] = Field(title="Nationality", json_schema_extra={"is_anonymized": True, "section": 5})
    complainant_informant_passport_no: Optional[str] = Field(title="Passport No.", json_schema_extra={"is_anonymized": True, "section": 5})
    complainant_informant_passport_date_of_issue: Optional[str] = Field(title="Date of Issue", json_schema_extra={"is_anonymized": True, "section": 5})
    complainant_informant_address: Optional[str] = Field(title="Address", json_schema_extra={"is_anonymized": True, "section": 5})
    complainant_informant_sex: Optional[str] = Field(title="Sex", json_schema_extra={"is_anonymized": True, "section": 5})
    complainant_informant_seen_occurrence: Optional[str] = Field(title="Whether complainant has seen the occurence or merely heard of it", json_schema_extra={"is_anonymized": True, "section": 5})
    accused_details: Optional[dict] = Field(title="Details of known/suspected/unknown accused with full particulars", json_schema_extra={"is_anonymized": True, "section": 6})
    victim_details: Optional[dict] = Field(title="Details of Victims with full particulars", json_schema_extra={"is_anonymized": True, "section": 7})
    stolen_property_details: Optional[dict] = Field(title="Particulars of Property stolen/involved with value", json_schema_extra={"is_anonymized": True, "section": 8})
    inquest_report_ud_case_no: Optional[str] = Field(title="Inquest Report/U.D. Case No. if any", json_schema_extra={"is_anonymized": True, "section": 9})
    fir_contents: Optional[str] = Field(title="F.I.R Contents", json_schema_extra={"is_anonymized": True, "section": 10})
    action_taken: Optional[str] = Field(title="Action Taken", json_schema_extra={"is_anonymized": True, "section": 11}),
    signature: str = Field(title="Signature/Thumb impression of the complainant", json_schema_extra={"is_anonymized": True, "section": 12})
    fir_dispatch_date_time: Optional[str] = Field(title="Date and time of dispatch to the Court", json_schema_extra={"is_anonymized": True, "section": 13})
    fir_carrier_name: Optional[str] = Field(title="Name of PC/HC who carried the FIR to the Court", json_schema_extra={"is_anonymized": True, "section": 14})
