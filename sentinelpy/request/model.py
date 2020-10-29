from enum import Enum
from typing import NamedTuple, Optional, Union


class SentinelProductRequest(NamedTuple):
    query: str
    rows: Optional[int]
    order_by: Optional[str]
    start: int
    username: str
    password: str


class PlatformName(Enum):
    SENTINEL_1 = "Sentinel-1"
    SENTINEL_2 = "Sentinel-2"
    SENTINEL_3 = "Sentinel-3"
    SENTINEL_5P = "Sentinel-5 Precursor"


class OrbitDirection(Enum):
    ASCENDING = "Ascending"
    DESCENDING = "Descending"


class PolarisationMode(Enum):
    HH = "HH"
    VV = "VV"
    HV = "HV"
    VH = "VH"
    HH_HV = "HH HV"
    VV_VH = "VV VH"


class SensorOperationalMode(Enum):
    SM = "SM"
    IW = "IW"
    EW = "EW"
    WV = "WV"


class SwathIdentifier(Enum):
    S1 = "S1"
    S2 = "S2"
    S3 = "S3"
    S4 = "S4"
    S5 = "S5"
    S6 = "S6"
    IW = "IW"
    IW1 = "IW1"
    IW2 = "IW2"
    IW3 = "IW3"
    EW = "EW"
    EW1 = "EW1"
    EW2 = "EW2"
    EW3 = "EW3"
    EW4 = "EW4"
    EW5 = "EW5"


class Timeliness(Enum):
    NRT = "NRT"
    STC = "STC"
    NTC = "NTC"


class Sentinel1ProductType(Enum):
    SLC = "SLC"
    GRD = "GRD"
    OCN = "OCN"


class Sentinel2ProductType(Enum):
    S2MSI2A = "S2MSI2A"
    S2MSI1C = "S2MSI1C"
    S2MS2Ap = "S2MS2Ap"


class Sentinel3ProductType(Enum):
    SR_1_SRA___ = "SR_1_SRA___"
    SR_1_SRA_A = "SR_1_SRA_A"
    SR_1_SRA_BS = "SR_1_SRA_BS"
    SR_2_LAN___ = "SR_2_LAN___"
    OL_1_EFR___ = "OL_1_EFR___"
    OL_1_ERR___ = "OL_1_ERR___"
    OL_2_LFR___ = "OL_2_LFR___"
    OL_2_LRR___ = "OL_2_LRR___"
    SL_1_RBT___ = "SL_1_RBT___"
    SL_2_LST___ = "SL_2_LST___"
    SY_2_SYN___ = "SY_2_SYN___"
    SY_2_V10___ = "SY_2_V10___"
    SY_2_VG1___ = "SY_2_VG1___"
    SY_2_VGP___ = "SY_2_VGP___"


class Sentinel5PProductType(Enum):
    L1B_IR_SIR = "L1B_IR_SIR"
    L1B_IR_UVN = "L1B_IR_UVN"
    L1B_RA_BD1 = "L1B_RA_BD1"
    L1B_RA_BD2 = "L1B_RA_BD2"
    L1B_RA_BD3 = "L1B_RA_BD3"
    L1B_RA_BD4 = "L1B_RA_BD4"
    L1B_RA_BD5 = "L1B_RA_BD5"
    L1B_RA_BD6 = "L1B_RA_BD6"
    L1B_RA_BD7 = "L1B_RA_BD7"
    L1B_RA_BD8 = "L1B_RA_BD8"
    L2__AER_AI = "L2__AER_AI"
    L2__AER_LH = "L2__AER_LH"
    L2__CH4 = "L2__CH4"
    L2__CLOUD_ = "L2__CLOUD_"
    L2__CO____ = "L2__CO____"
    L2__HCHO__ = "L2__HCHO__"
    L2__NO2___ = "L2__NO2___"
    L2__NP_BD3 = "L2__NP_BD3"
    L2__NP_BD6 = "L2__NP_BD6"
    L2__NP_BD7 = "L2__NP_BD7"
    L2__O3_TCL = "L2__O3_TCL"
    L2__O3____ = "L2__O3____"
    L2__SO2___ = "L2__SO2___"


ProductType = Union[
    Sentinel1ProductType,
    Sentinel2ProductType,
    Sentinel3ProductType,
    Sentinel5PProductType,
]


class FilterKeyword(Enum):
    PLATFORM_NAME = "platformname"
    BEGIN_POSITION = "beginposition"
    END_POSITION = "endposition"
    INGESTION_DATE = "ingestiondate"
    COLLECTION = "collection"
    FILE_NAME = "filename"
    FOOTPRINT = "footprint"
    ORBIT_NUMBER = "orbitnumber"
    LAST_ORBIT_NUMBER = "lastorbitnumber"
    RELATIVE_ORBIT_NUMBER = "relativeorbitnumber"
    LAST_RELATIVE_ORBIT_NUMBER = "lastrelativeorbitnumber"
    ORBIT_DIRECTION = "orbitdirection"
    POLARISATION_MODE = "polarisationmode"
    PRODUCT_TYPE = "producttype"
    SENSOR_OPERATIONAL_MODE = "sensoroperationalmode"
    SWATH_IDENTIFIER = "swathidentifier"
    CLOUD_COVER_PERCENTAGE = "cloudcoverpercentage"
    TIMELINESS = "timeliness"
