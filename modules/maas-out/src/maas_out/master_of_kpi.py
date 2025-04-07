# Here a a short example of usage opensearch py for complexe query

import logging
from maas_cds.model import CdsDataflow, CdsDatatake, CdsProduct
from opensearchpy import MultiSearch


def demo_extract():
    # Configure the logger
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Need to udate False to False
    # Remove also the response
    grafana_query = {
        "request": {
            "url": "api/ds/query?ds_type=elasticsearch&requestId=SQR104",
            "method": "POST",
            "data": {
                "queries": [
                    {
                        "alias": "dd_expected",
                        "bucketAggs": [
                            {
                                "field": "datatake_id",
                                "id": "3",
                                "settings": {
                                    "min_doc_count": "1",
                                    "order": "desc",
                                    "orderBy": "_term",
                                    "size": "0",
                                },
                                "type": "terms",
                            }
                        ],
                        "datasource": {
                            "type": "elasticsearch",
                            "uid": "P4E6B5BC91908CBD9",
                        },
                        "hide": False,
                        "metrics": [{"id": "1", "type": "count"}],
                        "query": 'mission: ("S1") AND satellite_unit: ("S1A") AND datatake_id: ("475292" OR "475293" OR "475294" OR "475295" OR "475296" OR "475297" OR "475298" OR "475299" OR "475300" OR "475301" OR "475302" OR "475303" OR "475304" OR "475305" OR "475306" OR "475307" OR "475308" OR "475309" OR "475310" OR "475311" OR "475312" OR "475313" OR "475314" OR "475315" OR "475316" OR "475317" OR "475318" OR "475319" OR "475320" OR "475321" OR "475322" OR "475323" OR "475324" OR "475325" OR "475326" OR "475327" OR "475328" OR "475329" OR "475330" OR "475331" OR "475332" OR "475333" OR "475334" OR "475335" OR "475336" OR "475337" OR "475338" OR "475339" OR "475340" OR "475341" OR "475342" OR "475343" OR "475344" OR "475345" OR "475346" OR "475347" OR "475348" OR "475349" OR "475350" OR "475351" OR "475352" OR "475353" OR "475354" OR "475355" OR "475356" OR "475357" OR "475358" OR "475359" OR "475360" OR "475361" OR "475362" OR "475363" OR "475364" OR "475365" OR "475366" OR "475367" OR "475368" OR "475369" OR "475370" OR "475371" OR "475372" OR "475373" OR "475374" OR "475375" OR "475376" OR "475377" OR "475378" OR "475379" OR "475380" OR "475381" OR "475382" OR "475383" OR "475384" OR "475385" OR "475386" OR "475387" OR "475388" OR "475389" OR "475390" OR "475391" OR "475392" OR "475393" OR "475394" OR "475395" OR "475396" OR "475397" OR "475398" OR "475399" OR "475400" OR "475401" OR "475402" OR "475403" OR "475404" OR "475405" OR "475406" OR "475407" OR "475408" OR "475409" OR "475410" OR "475411" OR "475412" OR "475413" OR "475414" OR "475415" OR "475416" OR "475417" OR "475418" OR "475419" OR "475420" OR "475421" OR "475422" OR "475423" OR "475424" OR "475425" OR "475426" OR "475427" OR "475428" OR "475429" OR "475430" OR "475431" OR "475432" OR "475433" OR "475434" OR "475435" OR "475436") AND product_type: ("EW_GRDM_1S" OR "EW_RAW__0A" OR "EW_RAW__0S" OR "EW_SLC__1A" OR "EW_SLC__1S" OR "IW_OCN__2A" OR "IW_RAW__0A" OR "IW_RAW__0N" OR "IW_SLC__1S" OR "N1_GRDF_1A" OR "N1_RAW__0S" OR "N3_GRDF_1A" OR "N3_SLC__1A" OR "N4_RAW__0S" OR "N5_GRDH_1A" OR "N6_GRDF_1A" OR "N6_GRDH_1A" OR "N6_GRDM_1A" OR "N6_RAW__0S" OR "S1_GRDM_1S" OR "S1_OCN__2A" OR "S1_SLC__1A" OR "S2_ETA__AX" OR "S2_RAW__0S" OR "S2_SLC__1A" OR "S3_GRDH_1A" OR "S3_GRDH_1S" OR "S3_OCN__2A" OR "S3_OCN__2S" OR "S3_RAW__0A" OR "S3_SLC__1S" OR "S4_ETA__AX" OR "S4_GRDF_1A" OR "S4_GRDH_1A" OR "S4_RAW__0A" OR "S4_RAW__0C" OR "S4_RAW__0N" OR "S5_ETA__AX" OR "S5_GRDH_1A" OR "S5_GRDM_1A" OR "S5_RAW__0A" OR "S6_GRDF_1S" OR "S6_GRDM_1A" OR "S6_GRDM_1S" OR "S6_OCN__2S" OR "S6_RAW__0A" OR "S6_RAW__0N" OR "S6_RAW__0S" OR "S6_SLC__1A" OR "WV_GRDH_1A" OR "WV_GRDM_1A" OR "WV_OCN__2S" OR "WV_RAW__0A" OR "WV_RAW__0C" OR "Z4_RAW__0S" OR "Z5_RAW__0S" OR "ZI_RAW__0S" OR "MSI_L1C_TC" OR "MSI_L1C_TL" OR "SL_1_RBT___" OR "SL_2_LST___" OR "SR_2_LAN_HY" OR "SR_2_LAN_LI" OR "SY_1_MISR__" OR "SY_2_VG1___" OR "AUX_BGO3__" OR "AUX_CTM_CO" OR "AUX_CTMCH4" OR "AUX_IERS_B" OR "AUX_IERS_C" OR "AUX_ISRF" OR "AUX_NISE" OR "NRTI_AUX_MET_2D" OR "NRTI_L1B_ENG_DB" OR "NRTI_L1B_RA_BD1" OR "NRTI_L1B_RA_BD3" OR "NRTI_L1B_RA_BD6" OR "NRTI_L1B_RA_BD8" OR "NRTI_L2__CLOUD_" OR "NRTI_L2__O3_TCL" OR "OFFL_AUX_MET_QP" OR "OFFL_L1B_RA_BD2" OR "OFFL_L2__AER_AI" OR "OFFL_L2__CH4___" OR "OFFL_L2__O3__PR" OR "OPER_AUX_CTMFCT" OR "OPER_L0__ENG_A_" OR "OPER_L0__ODB_1_" OR "OPER_L0__ODB_3_" OR "EW_ETA__AX" OR "MSI_L0__DS" OR "MSI_L1B_DS" OR "AISAUX" OR "AMH_ERRMAT" OR "AMV_ERRMAT" OR "EN_RAW__0S" OR "EW_GRDH_1S" OR "EW_OCN__2A" OR "EW_RAW__0C" OR "IW_GRDM_1A" OR "IW_GRDM_1S" OR "IW_RAW__0S" OR "N1_SLC__1A" OR "N2_GRDH_1A" OR "N2_RAW__0S" OR "N2_SLC__1A" OR "N3_GRDH_1A" OR "N3_RAW__0S" OR "N4_GRDF_1A" OR "N4_GRDH_1A" OR "N4_GRDM_1A" OR "N4_SLC__1A" OR "N5_GRDM_1A" OR "N5_RAW__0S" OR "N5_SLC__1A" OR "N6_SLC__1A" OR "RF_RAW__0S" OR "S1_ETA__AX" OR "S1_GRDF_1A" OR "S1_GRDF_1S" OR "S1_GRDH_1A" OR "S1_GRDH_1S" OR "S1_OCN__2S" OR "S1_RAW__0C" OR "S1_RAW__0S" OR "S1_SLC__1S" OR "S2_GRDF_1A" OR "S2_GRDH_1S" OR "S2_GRDM_1A" OR "S2_GRDM_1S" OR "S2_OCN__2A" OR "S2_RAW__0A" OR "S2_RAW__0C" OR "S2_SLC__1S" OR "S3_ETA__AX" OR "S3_GRDM_1A" OR "S3_GRDM_1S" OR "S3_RAW__0C" OR "S3_RAW__0N" OR "S3_RAW__0S" OR "S3_SLC__1A" OR "S4_GRDH_1S" OR "S4_GRDM_1A" OR "S4_SLC__1A" OR "S4_SLC__1S" OR "S5_GRDF_1S" OR "S5_OCN__2S" OR "S5_RAW__0S" OR "S5_SLC__1A" OR "S6_ETA__AX" OR "S6_GRDH_1S" OR "S6_OCN__2A" OR "S6_RAW__0C" OR "WV_GRDM_1S" OR "WV_OCN__2A" OR "WV_SLC__1A" OR "WV_SLC__1S" OR "Z2_RAW__0S" OR "Z3_RAW__0S" OR "Z6_RAW__0S" OR "ZW_RAW__0S" OR "MSI_L1C_DS" OR "MSI_L2A_DS" OR "MSI_L2A_TC" OR "MSI_L2A_TL" OR "MW_1_MON_AX" OR "OL_1_EFR___" OR "SL_2_FRP___" OR "SR_1_CA2CAX" OR "SR_1_SRA___" OR "SR_1_SRA_BS" OR "SR_2_LAN_SI" OR "SY_2_AOD___" OR "SY_2_SYN___" OR "SY_2_V10___" OR "AUX_BGCLD_" OR "ICM_CKDSIR" OR "ICM_CKDUVN" OR "NRTI_AUX_MET_TP" OR "NRTI_L1B_RA_BD2" OR "NRTI_L1B_RA_BD4" OR "NRTI_L1B_RA_BD5" OR "NRTI_L2__CO____" OR "OFFL_AUX_MET_2D" OR "OFFL_AUX_MET_TP" OR "OFFL_ICM_CA_SIR" OR "OFFL_L1B_CA_SIR" OR "OFFL_L1B_ENG_DB" OR "OFFL_L1B_IR_UVN" OR "OFFL_L1B_RA_BD4" OR "OFFL_L1B_RA_BD5" OR "OFFL_L1B_RA_BD8" OR "OFFL_L2__AER_LH" OR "OFFL_L2__CO____" OR "OFFL_L2__HCHO__" OR "OFFL_L2__NO2___" OR "OFFL_L2__NP_BD3" OR "OFFL_L2__NP_BD6" OR "OFFL_L2__NP_BD7" OR "OPER_AUX_CTMANA" OR "OPER_L0__ODB_4_" OR "OPER_L0__ODB_7_" OR "OPER_L0__PDQ___" OR "ZE_RAW__0S" OR "___OBS__SS" OR "EW_GRDH_1A" OR "EW_GRDM_1A" OR "EW_OCN__2S" OR "EW_RAW__0N" OR "IW_ETA__AX" OR "IW_GRDH_1A" OR "IW_GRDH_1S" OR "IW_OCN__2S" OR "IW_RAW__0C" OR "IW_SLC__1A" OR "N1_GRDH_1A" OR "N1_GRDM_1A" OR "N2_GRDF_1A" OR "N2_GRDM_1A" OR "N3_GRDM_1A" OR "N5_GRDF_1A" OR "S1_GRDM_1A" OR "S1_RAW__0A" OR "S1_RAW__0N" OR "S2_GRDF_1S" OR "S2_GRDH_1A" OR "S2_OCN__2S" OR "S2_RAW__0N" OR "S3_GRDF_1A" OR "S3_GRDF_1S" OR "S4_GRDF_1S" OR "S4_GRDM_1S" OR "S4_OCN__2A" OR "S4_OCN__2S" OR "S4_RAW__0S" OR "S5_GRDF_1A" OR "S5_GRDH_1S" OR "S5_GRDM_1S" OR "S5_OCN__2A" OR "S5_RAW__0C" OR "S5_RAW__0N" OR "S5_SLC__1S" OR "S6_GRDF_1A" OR "S6_GRDH_1A" OR "S6_SLC__1S" OR "WV_GRDH_1S" OR "WV_RAW__0N" OR "WV_RAW__0S" OR "Z1_RAW__0S" OR "Z7_RAW__0S" OR "MW_1_DNB_AX" OR "MW_1_NIR_AX" OR "OL_1_ERR___" OR "OL_2_LFR___" OR "OL_2_LRR___" OR "SL_1_VSC_AX" OR "SR_1_CA1LAX" OR "SR_1_CA1SAX" OR "SR_1_CA2KAX" OR "SR_1_SRA_A_" OR "SR_2_LAN___" OR "SY_2_VGP___" OR "AUX_BGHCHO" OR "AUX_BGSO2_" OR "AUX_L1_CKD" OR "AUX_O3_M" OR "NRTI_AUX_MET_QP" OR "NRTI_L1B_RA_BD7" OR "NRTI_L2__AER_AI" OR "NRTI_L2__AER_LH" OR "NRTI_L2__FRESCO" OR "NRTI_L2__HCHO__" OR "NRTI_L2__NO2___" OR "NRTI_L2__O3____" OR "NRTI_L2__O3__PR" OR "NRTI_L2__SO2___" OR "OFFL_ICM_CA_UVN" OR "OFFL_L1B_CA_UVN" OR "OFFL_L1B_IR_SIR" OR "OFFL_L1B_RA_BD1" OR "OFFL_L1B_RA_BD3" OR "OFFL_L1B_RA_BD6" OR "OFFL_L1B_RA_BD7" OR "OFFL_L2__CLOUD_" OR "OFFL_L2__FRESCO" OR "OFFL_L2__O3____" OR "OFFL_L2__O3_TCL" OR "OFFL_L2__SO2___" OR "OPER_L0__ODB_2_" OR "OPER_L0__ODB_5_" OR "OPER_L0__ODB_6_" OR "OPER_L0__ODB_8_" OR "OPER_L0__SAT_A_" OR "MSI_L1A_DS" OR "MSI_L0__GR" OR "MSI_L1A_GR" OR "MSI_L1B_GR" OR "AUX_ML2" OR "AI_RAW__0_") ',
                        "refId": "PRIP for DD",
                        "timeField": "sensing_start_date",
                        "datasourceId": 4,
                        "intervalMs": 86400000,
                        "maxDataPoints": 1,
                    },
                    {
                        "alias": "dd_produced",
                        "bucketAggs": [
                            {
                                "field": "datatake_id",
                                "id": "3",
                                "settings": {
                                    "min_doc_count": "1",
                                    "order": "desc",
                                    "orderBy": "_term",
                                    "size": "0",
                                },
                                "type": "terms",
                            }
                        ],
                        "datasource": {
                            "type": "elasticsearch",
                            "uid": "P4E6B5BC91908CBD9",
                        },
                        "hide": False,
                        "metrics": [{"id": "1", "type": "count"}],
                        "query": 'mission: ("S1") AND satellite_unit: ("S1A") AND datatake_id: ("475292" OR "475293" OR "475294" OR "475295" OR "475296" OR "475297" OR "475298" OR "475299" OR "475300" OR "475301" OR "475302" OR "475303" OR "475304" OR "475305" OR "475306" OR "475307" OR "475308" OR "475309" OR "475310" OR "475311" OR "475312" OR "475313" OR "475314" OR "475315" OR "475316" OR "475317" OR "475318" OR "475319" OR "475320" OR "475321" OR "475322" OR "475323" OR "475324" OR "475325" OR "475326" OR "475327" OR "475328" OR "475329" OR "475330" OR "475331" OR "475332" OR "475333" OR "475334" OR "475335" OR "475336" OR "475337" OR "475338" OR "475339" OR "475340" OR "475341" OR "475342" OR "475343" OR "475344" OR "475345" OR "475346" OR "475347" OR "475348" OR "475349" OR "475350" OR "475351" OR "475352" OR "475353" OR "475354" OR "475355" OR "475356" OR "475357" OR "475358" OR "475359" OR "475360" OR "475361" OR "475362" OR "475363" OR "475364" OR "475365" OR "475366" OR "475367" OR "475368" OR "475369" OR "475370" OR "475371" OR "475372" OR "475373" OR "475374" OR "475375" OR "475376" OR "475377" OR "475378" OR "475379" OR "475380" OR "475381" OR "475382" OR "475383" OR "475384" OR "475385" OR "475386" OR "475387" OR "475388" OR "475389" OR "475390" OR "475391" OR "475392" OR "475393" OR "475394" OR "475395" OR "475396" OR "475397" OR "475398" OR "475399" OR "475400" OR "475401" OR "475402" OR "475403" OR "475404" OR "475405" OR "475406" OR "475407" OR "475408" OR "475409" OR "475410" OR "475411" OR "475412" OR "475413" OR "475414" OR "475415" OR "475416" OR "475417" OR "475418" OR "475419" OR "475420" OR "475421" OR "475422" OR "475423" OR "475424" OR "475425" OR "475426" OR "475427" OR "475428" OR "475429" OR "475430" OR "475431" OR "475432" OR "475433" OR "475434" OR "475435" OR "475436") AND product_type: ("EW_GRDM_1S" OR "EW_RAW__0A" OR "EW_RAW__0S" OR "EW_SLC__1A" OR "EW_SLC__1S" OR "IW_OCN__2A" OR "IW_RAW__0A" OR "IW_RAW__0N" OR "IW_SLC__1S" OR "N1_GRDF_1A" OR "N1_RAW__0S" OR "N3_GRDF_1A" OR "N3_SLC__1A" OR "N4_RAW__0S" OR "N5_GRDH_1A" OR "N6_GRDF_1A" OR "N6_GRDH_1A" OR "N6_GRDM_1A" OR "N6_RAW__0S" OR "S1_GRDM_1S" OR "S1_OCN__2A" OR "S1_SLC__1A" OR "S2_ETA__AX" OR "S2_RAW__0S" OR "S2_SLC__1A" OR "S3_GRDH_1A" OR "S3_GRDH_1S" OR "S3_OCN__2A" OR "S3_OCN__2S" OR "S3_RAW__0A" OR "S3_SLC__1S" OR "S4_ETA__AX" OR "S4_GRDF_1A" OR "S4_GRDH_1A" OR "S4_RAW__0A" OR "S4_RAW__0C" OR "S4_RAW__0N" OR "S5_ETA__AX" OR "S5_GRDH_1A" OR "S5_GRDM_1A" OR "S5_RAW__0A" OR "S6_GRDF_1S" OR "S6_GRDM_1A" OR "S6_GRDM_1S" OR "S6_OCN__2S" OR "S6_RAW__0A" OR "S6_RAW__0N" OR "S6_RAW__0S" OR "S6_SLC__1A" OR "WV_GRDH_1A" OR "WV_GRDM_1A" OR "WV_OCN__2S" OR "WV_RAW__0A" OR "WV_RAW__0C" OR "Z4_RAW__0S" OR "Z5_RAW__0S" OR "ZI_RAW__0S" OR "MSI_L1C_TC" OR "MSI_L1C_TL" OR "SL_1_RBT___" OR "SL_2_LST___" OR "SR_2_LAN_HY" OR "SR_2_LAN_LI" OR "SY_1_MISR__" OR "SY_2_VG1___" OR "AUX_BGO3__" OR "AUX_CTM_CO" OR "AUX_CTMCH4" OR "AUX_IERS_B" OR "AUX_IERS_C" OR "AUX_ISRF" OR "AUX_NISE" OR "NRTI_AUX_MET_2D" OR "NRTI_L1B_ENG_DB" OR "NRTI_L1B_RA_BD1" OR "NRTI_L1B_RA_BD3" OR "NRTI_L1B_RA_BD6" OR "NRTI_L1B_RA_BD8" OR "NRTI_L2__CLOUD_" OR "NRTI_L2__O3_TCL" OR "OFFL_AUX_MET_QP" OR "OFFL_L1B_RA_BD2" OR "OFFL_L2__AER_AI" OR "OFFL_L2__CH4___" OR "OFFL_L2__O3__PR" OR "OPER_AUX_CTMFCT" OR "OPER_L0__ENG_A_" OR "OPER_L0__ODB_1_" OR "OPER_L0__ODB_3_" OR "EW_ETA__AX" OR "MSI_L0__DS" OR "MSI_L1B_DS" OR "AISAUX" OR "AMH_ERRMAT" OR "AMV_ERRMAT" OR "EN_RAW__0S" OR "EW_GRDH_1S" OR "EW_OCN__2A" OR "EW_RAW__0C" OR "IW_GRDM_1A" OR "IW_GRDM_1S" OR "IW_RAW__0S" OR "N1_SLC__1A" OR "N2_GRDH_1A" OR "N2_RAW__0S" OR "N2_SLC__1A" OR "N3_GRDH_1A" OR "N3_RAW__0S" OR "N4_GRDF_1A" OR "N4_GRDH_1A" OR "N4_GRDM_1A" OR "N4_SLC__1A" OR "N5_GRDM_1A" OR "N5_RAW__0S" OR "N5_SLC__1A" OR "N6_SLC__1A" OR "RF_RAW__0S" OR "S1_ETA__AX" OR "S1_GRDF_1A" OR "S1_GRDF_1S" OR "S1_GRDH_1A" OR "S1_GRDH_1S" OR "S1_OCN__2S" OR "S1_RAW__0C" OR "S1_RAW__0S" OR "S1_SLC__1S" OR "S2_GRDF_1A" OR "S2_GRDH_1S" OR "S2_GRDM_1A" OR "S2_GRDM_1S" OR "S2_OCN__2A" OR "S2_RAW__0A" OR "S2_RAW__0C" OR "S2_SLC__1S" OR "S3_ETA__AX" OR "S3_GRDM_1A" OR "S3_GRDM_1S" OR "S3_RAW__0C" OR "S3_RAW__0N" OR "S3_RAW__0S" OR "S3_SLC__1A" OR "S4_GRDH_1S" OR "S4_GRDM_1A" OR "S4_SLC__1A" OR "S4_SLC__1S" OR "S5_GRDF_1S" OR "S5_OCN__2S" OR "S5_RAW__0S" OR "S5_SLC__1A" OR "S6_ETA__AX" OR "S6_GRDH_1S" OR "S6_OCN__2A" OR "S6_RAW__0C" OR "WV_GRDM_1S" OR "WV_OCN__2A" OR "WV_SLC__1A" OR "WV_SLC__1S" OR "Z2_RAW__0S" OR "Z3_RAW__0S" OR "Z6_RAW__0S" OR "ZW_RAW__0S" OR "MSI_L1C_DS" OR "MSI_L2A_DS" OR "MSI_L2A_TC" OR "MSI_L2A_TL" OR "MW_1_MON_AX" OR "OL_1_EFR___" OR "SL_2_FRP___" OR "SR_1_CA2CAX" OR "SR_1_SRA___" OR "SR_1_SRA_BS" OR "SR_2_LAN_SI" OR "SY_2_AOD___" OR "SY_2_SYN___" OR "SY_2_V10___" OR "AUX_BGCLD_" OR "ICM_CKDSIR" OR "ICM_CKDUVN" OR "NRTI_AUX_MET_TP" OR "NRTI_L1B_RA_BD2" OR "NRTI_L1B_RA_BD4" OR "NRTI_L1B_RA_BD5" OR "NRTI_L2__CO____" OR "OFFL_AUX_MET_2D" OR "OFFL_AUX_MET_TP" OR "OFFL_ICM_CA_SIR" OR "OFFL_L1B_CA_SIR" OR "OFFL_L1B_ENG_DB" OR "OFFL_L1B_IR_UVN" OR "OFFL_L1B_RA_BD4" OR "OFFL_L1B_RA_BD5" OR "OFFL_L1B_RA_BD8" OR "OFFL_L2__AER_LH" OR "OFFL_L2__CO____" OR "OFFL_L2__HCHO__" OR "OFFL_L2__NO2___" OR "OFFL_L2__NP_BD3" OR "OFFL_L2__NP_BD6" OR "OFFL_L2__NP_BD7" OR "OPER_AUX_CTMANA" OR "OPER_L0__ODB_4_" OR "OPER_L0__ODB_7_" OR "OPER_L0__PDQ___" OR "ZE_RAW__0S" OR "___OBS__SS" OR "EW_GRDH_1A" OR "EW_GRDM_1A" OR "EW_OCN__2S" OR "EW_RAW__0N" OR "IW_ETA__AX" OR "IW_GRDH_1A" OR "IW_GRDH_1S" OR "IW_OCN__2S" OR "IW_RAW__0C" OR "IW_SLC__1A" OR "N1_GRDH_1A" OR "N1_GRDM_1A" OR "N2_GRDF_1A" OR "N2_GRDM_1A" OR "N3_GRDM_1A" OR "N5_GRDF_1A" OR "S1_GRDM_1A" OR "S1_RAW__0A" OR "S1_RAW__0N" OR "S2_GRDF_1S" OR "S2_GRDH_1A" OR "S2_OCN__2S" OR "S2_RAW__0N" OR "S3_GRDF_1A" OR "S3_GRDF_1S" OR "S4_GRDF_1S" OR "S4_GRDM_1S" OR "S4_OCN__2A" OR "S4_OCN__2S" OR "S4_RAW__0S" OR "S5_GRDF_1A" OR "S5_GRDH_1S" OR "S5_GRDM_1S" OR "S5_OCN__2A" OR "S5_RAW__0C" OR "S5_RAW__0N" OR "S5_SLC__1S" OR "S6_GRDF_1A" OR "S6_GRDH_1A" OR "S6_SLC__1S" OR "WV_GRDH_1S" OR "WV_RAW__0N" OR "WV_RAW__0S" OR "Z1_RAW__0S" OR "Z7_RAW__0S" OR "MW_1_DNB_AX" OR "MW_1_NIR_AX" OR "OL_1_ERR___" OR "OL_2_LFR___" OR "OL_2_LRR___" OR "SL_1_VSC_AX" OR "SR_1_CA1LAX" OR "SR_1_CA1SAX" OR "SR_1_CA2KAX" OR "SR_1_SRA_A_" OR "SR_2_LAN___" OR "SY_2_VGP___" OR "AUX_BGHCHO" OR "AUX_BGSO2_" OR "AUX_L1_CKD" OR "AUX_O3_M" OR "NRTI_AUX_MET_QP" OR "NRTI_L1B_RA_BD7" OR "NRTI_L2__AER_AI" OR "NRTI_L2__AER_LH" OR "NRTI_L2__FRESCO" OR "NRTI_L2__HCHO__" OR "NRTI_L2__NO2___" OR "NRTI_L2__O3____" OR "NRTI_L2__O3__PR" OR "NRTI_L2__SO2___" OR "OFFL_ICM_CA_UVN" OR "OFFL_L1B_CA_UVN" OR "OFFL_L1B_IR_SIR" OR "OFFL_L1B_RA_BD1" OR "OFFL_L1B_RA_BD3" OR "OFFL_L1B_RA_BD6" OR "OFFL_L1B_RA_BD7" OR "OFFL_L2__CLOUD_" OR "OFFL_L2__FRESCO" OR "OFFL_L2__O3____" OR "OFFL_L2__O3_TCL" OR "OFFL_L2__SO2___" OR "OPER_L0__ODB_2_" OR "OPER_L0__ODB_5_" OR "OPER_L0__ODB_6_" OR "OPER_L0__ODB_8_" OR "OPER_L0__SAT_A_" OR "MSI_L1A_DS" OR "MSI_L0__GR" OR "MSI_L1A_GR" OR "MSI_L1B_GR" OR "AUX_ML2" OR "AI_RAW__0_") AND nb_dd_served: [0 TO *]',
                        "refId": "DD from PRIP",
                        "timeField": "sensing_start_date",
                        "datasourceId": 4,
                        "intervalMs": 86400000,
                        "maxDataPoints": 1,
                    },
                    {
                        "alias": "lta_expected",
                        "bucketAggs": [
                            {
                                "field": "datatake_id",
                                "id": "2",
                                "settings": {
                                    "min_doc_count": "1",
                                    "order": "desc",
                                    "orderBy": "_term",
                                    "size": "0",
                                },
                                "type": "terms",
                            }
                        ],
                        "datasource": {
                            "type": "elasticsearch",
                            "uid": "P4E6B5BC91908CBD9",
                        },
                        "hide": False,
                        "metrics": [{"id": "1", "type": "count"}],
                        "query": 'mission: ("S1") AND satellite_unit: ("S1A") AND datatake_id: ("475292" OR "475293" OR "475294" OR "475295" OR "475296" OR "475297" OR "475298" OR "475299" OR "475300" OR "475301" OR "475302" OR "475303" OR "475304" OR "475305" OR "475306" OR "475307" OR "475308" OR "475309" OR "475310" OR "475311" OR "475312" OR "475313" OR "475314" OR "475315" OR "475316" OR "475317" OR "475318" OR "475319" OR "475320" OR "475321" OR "475322" OR "475323" OR "475324" OR "475325" OR "475326" OR "475327" OR "475328" OR "475329" OR "475330" OR "475331" OR "475332" OR "475333" OR "475334" OR "475335" OR "475336" OR "475337" OR "475338" OR "475339" OR "475340" OR "475341" OR "475342" OR "475343" OR "475344" OR "475345" OR "475346" OR "475347" OR "475348" OR "475349" OR "475350" OR "475351" OR "475352" OR "475353" OR "475354" OR "475355" OR "475356" OR "475357" OR "475358" OR "475359" OR "475360" OR "475361" OR "475362" OR "475363" OR "475364" OR "475365" OR "475366" OR "475367" OR "475368" OR "475369" OR "475370" OR "475371" OR "475372" OR "475373" OR "475374" OR "475375" OR "475376" OR "475377" OR "475378" OR "475379" OR "475380" OR "475381" OR "475382" OR "475383" OR "475384" OR "475385" OR "475386" OR "475387" OR "475388" OR "475389" OR "475390" OR "475391" OR "475392" OR "475393" OR "475394" OR "475395" OR "475396" OR "475397" OR "475398" OR "475399" OR "475400" OR "475401" OR "475402" OR "475403" OR "475404" OR "475405" OR "475406" OR "475407" OR "475408" OR "475409" OR "475410" OR "475411" OR "475412" OR "475413" OR "475414" OR "475415" OR "475416" OR "475417" OR "475418" OR "475419" OR "475420" OR "475421" OR "475422" OR "475423" OR "475424" OR "475425" OR "475426" OR "475427" OR "475428" OR "475429" OR "475430" OR "475431" OR "475432" OR "475433" OR "475434" OR "475435" OR "475436") AND product_type: ("EW_RAW__0A" OR "EW_RAW__0S" OR "HK_RAW__0_" OR "IW_RAW__0A" OR "IW_RAW__0N" OR "N1_RAW__0S" OR "N4_RAW__0S" OR "N6_RAW__0S" OR "S2_ETA__AX" OR "S2_RAW__0S" OR "S3_RAW__0A" OR "S4_ETA__AX" OR "S4_RAW__0A" OR "S4_RAW__0C" OR "S4_RAW__0N" OR "S5_ETA__AX" OR "S5_RAW__0A" OR "S6_RAW__0A" OR "S6_RAW__0N" OR "S6_RAW__0S" OR "WV_RAW__0A" OR "WV_RAW__0C" OR "Z4_RAW__0S" OR "Z5_RAW__0S" OR "ZI_RAW__0S" OR "DO_0_NAV___" OR "MW_1_CAL___" OR "OL_0_CR0___" OR "OL_0_CR1___" OR "SL_0_SLT___" OR "TM_0_HKM___" OR "TM_0_HKM2__" OR "AUX_BGO3__" OR "AUX_CTM_CO" OR "AUX_CTMCH4" OR "AUX_IERS_B" OR "AUX_IERS_C" OR "AUX_ISRF" OR "AUX_NISE" OR "NRTI_AUX_MET_2D" OR "NRTI_L1B_ENG_DB" OR "NRTI_L1B_RA_BD1" OR "NRTI_L1B_RA_BD3" OR "NRTI_L1B_RA_BD6" OR "NRTI_L1B_RA_BD8" OR "NRTI_L2__CLOUD_" OR "NRTI_L2__O3_TCL" OR "OFFL_AUX_MET_QP" OR "OFFL_L1B_RA_BD2" OR "OFFL_L2__AER_AI" OR "OFFL_L2__CH4___" OR "OFFL_L2__O3__PR" OR "OPER_AUX_CTMFCT" OR "OPER_L0__ENG_A_" OR "OPER_L0__ODB_1_" OR "OPER_L0__ODB_3_" OR "EW_ETA__AX" OR "MSI_L0__DS" OR "AISAUX" OR "AMH_ERRMAT" OR "AMV_ERRMAT" OR "EN_RAW__0S" OR "EW_RAW__0C" OR "GP_RAW__0_" OR "IW_RAW__0S" OR "N2_RAW__0S" OR "N3_RAW__0S" OR "N5_RAW__0S" OR "RF_RAW__0S" OR "S1_ETA__AX" OR "S1_RAW__0C" OR "S1_RAW__0S" OR "S2_RAW__0A" OR "S2_RAW__0C" OR "S3_ETA__AX" OR "S3_RAW__0C" OR "S3_RAW__0N" OR "S3_RAW__0S" OR "S5_RAW__0S" OR "S6_ETA__AX" OR "S6_RAW__0C" OR "Z2_RAW__0S" OR "Z3_RAW__0S" OR "Z6_RAW__0S" OR "ZW_RAW__0S" OR "AUX_SADATA" OR "PRD_HKTM__" OR "MW_0_MWR___" OR "MW_1_MON_AX" OR "SR_0_SRA___" OR "SR_1_CA2CAX" OR "SR_1_CAL___" OR "TM_0_NAT___" OR "AUX_BGCLD_" OR "ICM_CKDSIR" OR "ICM_CKDUVN" OR "NRTI_AUX_MET_TP" OR "NRTI_L1B_RA_BD2" OR "NRTI_L1B_RA_BD4" OR "NRTI_L1B_RA_BD5" OR "NRTI_L2__CO____" OR "OFFL_AUX_MET_2D" OR "OFFL_AUX_MET_TP" OR "OFFL_ICM_CA_SIR" OR "OFFL_L1B_CA_SIR" OR "OFFL_L1B_ENG_DB" OR "OFFL_L1B_IR_UVN" OR "OFFL_L1B_RA_BD4" OR "OFFL_L1B_RA_BD5" OR "OFFL_L1B_RA_BD8" OR "OFFL_L2__AER_LH" OR "OFFL_L2__CO____" OR "OFFL_L2__HCHO__" OR "OFFL_L2__NO2___" OR "OFFL_L2__NP_BD3" OR "OFFL_L2__NP_BD6" OR "OFFL_L2__NP_BD7" OR "OPER_AUX_CTMANA" OR "OPER_L0__ODB_4_" OR "OPER_L0__ODB_7_" OR "OPER_L0__PDQ___" OR "ZE_RAW__0S" OR "EW_RAW__0N" OR "IW_ETA__AX" OR "IW_RAW__0C" OR "S1_RAW__0A" OR "S1_RAW__0N" OR "S2_RAW__0N" OR "S4_RAW__0S" OR "S5_RAW__0C" OR "S5_RAW__0N" OR "WV_RAW__0N" OR "WV_RAW__0S" OR "Z1_RAW__0S" OR "Z7_RAW__0S" OR "DO_0_DOP___" OR "GN_0_GNS___" OR "MW_1_DNB_AX" OR "MW_1_NIR_AX" OR "OL_0_EFR___" OR "OL_1_RAC___" OR "OL_1_SPC___" OR "SL_1_VSC_AX" OR "SR_0_CAL___" OR "SR_1_CA1LAX" OR "SR_1_CA1SAX" OR "SR_1_CA2KAX" OR "AUX_BGHCHO" OR "AUX_BGSO2_" OR "AUX_L1_CKD" OR "AUX_O3_M" OR "NRTI_AUX_MET_QP" OR "NRTI_L1B_RA_BD7" OR "NRTI_L2__AER_AI" OR "NRTI_L2__AER_LH" OR "NRTI_L2__HCHO__" OR "NRTI_L2__NO2___" OR "NRTI_L2__O3____" OR "NRTI_L2__O3__PR" OR "NRTI_L2__SO2___" OR "OFFL_ICM_CA_UVN" OR "OFFL_L1B_CA_UVN" OR "OFFL_L1B_IR_SIR" OR "OFFL_L1B_RA_BD1" OR "OFFL_L1B_RA_BD3" OR "OFFL_L1B_RA_BD6" OR "OFFL_L1B_RA_BD7" OR "OFFL_L2__CLOUD_" OR "OFFL_L2__FRESCO" OR "OFFL_L2__O3____" OR "OFFL_L2__O3_TCL" OR "OFFL_L2__SO2___" OR "OPER_L0__ODB_2_" OR "OPER_L0__ODB_5_" OR "OPER_L0__ODB_6_" OR "OPER_L0__ODB_8_" OR "OPER_L0__SAT_A_" OR "AUX_O3PPWL" OR "MSI_L0__GR" OR "AUX_ML2" OR "AI_RAW__0_")',
                        "refId": "PRIP for LTA",
                        "timeField": "sensing_start_date",
                        "datasourceId": 4,
                        "intervalMs": 86400000,
                        "maxDataPoints": 1,
                    },
                    {
                        "alias": "lta_produced",
                        "bucketAggs": [
                            {
                                "field": "datatake_id",
                                "id": "3",
                                "settings": {
                                    "min_doc_count": "1",
                                    "missing": "0",
                                    "order": "desc",
                                    "orderBy": "_term",
                                    "size": "0",
                                },
                                "type": "terms",
                            }
                        ],
                        "datasource": {
                            "type": "elasticsearch",
                            "uid": "P4E6B5BC91908CBD9",
                        },
                        "hide": False,
                        "metrics": [{"id": "1", "type": "count"}],
                        "query": 'mission: ("S1") AND satellite_unit: ("S1A") AND datatake_id: ("475292" OR "475293" OR "475294" OR "475295" OR "475296" OR "475297" OR "475298" OR "475299" OR "475300" OR "475301" OR "475302" OR "475303" OR "475304" OR "475305" OR "475306" OR "475307" OR "475308" OR "475309" OR "475310" OR "475311" OR "475312" OR "475313" OR "475314" OR "475315" OR "475316" OR "475317" OR "475318" OR "475319" OR "475320" OR "475321" OR "475322" OR "475323" OR "475324" OR "475325" OR "475326" OR "475327" OR "475328" OR "475329" OR "475330" OR "475331" OR "475332" OR "475333" OR "475334" OR "475335" OR "475336" OR "475337" OR "475338" OR "475339" OR "475340" OR "475341" OR "475342" OR "475343" OR "475344" OR "475345" OR "475346" OR "475347" OR "475348" OR "475349" OR "475350" OR "475351" OR "475352" OR "475353" OR "475354" OR "475355" OR "475356" OR "475357" OR "475358" OR "475359" OR "475360" OR "475361" OR "475362" OR "475363" OR "475364" OR "475365" OR "475366" OR "475367" OR "475368" OR "475369" OR "475370" OR "475371" OR "475372" OR "475373" OR "475374" OR "475375" OR "475376" OR "475377" OR "475378" OR "475379" OR "475380" OR "475381" OR "475382" OR "475383" OR "475384" OR "475385" OR "475386" OR "475387" OR "475388" OR "475389" OR "475390" OR "475391" OR "475392" OR "475393" OR "475394" OR "475395" OR "475396" OR "475397" OR "475398" OR "475399" OR "475400" OR "475401" OR "475402" OR "475403" OR "475404" OR "475405" OR "475406" OR "475407" OR "475408" OR "475409" OR "475410" OR "475411" OR "475412" OR "475413" OR "475414" OR "475415" OR "475416" OR "475417" OR "475418" OR "475419" OR "475420" OR "475421" OR "475422" OR "475423" OR "475424" OR "475425" OR "475426" OR "475427" OR "475428" OR "475429" OR "475430" OR "475431" OR "475432" OR "475433" OR "475434" OR "475435" OR "475436") AND product_type: ("EW_RAW__0A" OR "EW_RAW__0S" OR "HK_RAW__0_" OR "IW_RAW__0A" OR "IW_RAW__0N" OR "N1_RAW__0S" OR "N4_RAW__0S" OR "N6_RAW__0S" OR "S2_ETA__AX" OR "S2_RAW__0S" OR "S3_RAW__0A" OR "S4_ETA__AX" OR "S4_RAW__0A" OR "S4_RAW__0C" OR "S4_RAW__0N" OR "S5_ETA__AX" OR "S5_RAW__0A" OR "S6_RAW__0A" OR "S6_RAW__0N" OR "S6_RAW__0S" OR "WV_RAW__0A" OR "WV_RAW__0C" OR "Z4_RAW__0S" OR "Z5_RAW__0S" OR "ZI_RAW__0S" OR "DO_0_NAV___" OR "MW_1_CAL___" OR "OL_0_CR0___" OR "OL_0_CR1___" OR "SL_0_SLT___" OR "TM_0_HKM___" OR "TM_0_HKM2__" OR "AUX_BGO3__" OR "AUX_CTM_CO" OR "AUX_CTMCH4" OR "AUX_IERS_B" OR "AUX_IERS_C" OR "AUX_ISRF" OR "AUX_NISE" OR "NRTI_AUX_MET_2D" OR "NRTI_L1B_ENG_DB" OR "NRTI_L1B_RA_BD1" OR "NRTI_L1B_RA_BD3" OR "NRTI_L1B_RA_BD6" OR "NRTI_L1B_RA_BD8" OR "NRTI_L2__CLOUD_" OR "NRTI_L2__O3_TCL" OR "OFFL_AUX_MET_QP" OR "OFFL_L1B_RA_BD2" OR "OFFL_L2__AER_AI" OR "OFFL_L2__CH4___" OR "OFFL_L2__O3__PR" OR "OPER_AUX_CTMFCT" OR "OPER_L0__ENG_A_" OR "OPER_L0__ODB_1_" OR "OPER_L0__ODB_3_" OR "EW_ETA__AX" OR "MSI_L0__DS" OR "AISAUX" OR "AMH_ERRMAT" OR "AMV_ERRMAT" OR "EN_RAW__0S" OR "EW_RAW__0C" OR "GP_RAW__0_" OR "IW_RAW__0S" OR "N2_RAW__0S" OR "N3_RAW__0S" OR "N5_RAW__0S" OR "RF_RAW__0S" OR "S1_ETA__AX" OR "S1_RAW__0C" OR "S1_RAW__0S" OR "S2_RAW__0A" OR "S2_RAW__0C" OR "S3_ETA__AX" OR "S3_RAW__0C" OR "S3_RAW__0N" OR "S3_RAW__0S" OR "S5_RAW__0S" OR "S6_ETA__AX" OR "S6_RAW__0C" OR "Z2_RAW__0S" OR "Z3_RAW__0S" OR "Z6_RAW__0S" OR "ZW_RAW__0S" OR "AUX_SADATA" OR "PRD_HKTM__" OR "MW_0_MWR___" OR "MW_1_MON_AX" OR "SR_0_SRA___" OR "SR_1_CA2CAX" OR "SR_1_CAL___" OR "TM_0_NAT___" OR "AUX_BGCLD_" OR "ICM_CKDSIR" OR "ICM_CKDUVN" OR "NRTI_AUX_MET_TP" OR "NRTI_L1B_RA_BD2" OR "NRTI_L1B_RA_BD4" OR "NRTI_L1B_RA_BD5" OR "NRTI_L2__CO____" OR "OFFL_AUX_MET_2D" OR "OFFL_AUX_MET_TP" OR "OFFL_ICM_CA_SIR" OR "OFFL_L1B_CA_SIR" OR "OFFL_L1B_ENG_DB" OR "OFFL_L1B_IR_UVN" OR "OFFL_L1B_RA_BD4" OR "OFFL_L1B_RA_BD5" OR "OFFL_L1B_RA_BD8" OR "OFFL_L2__AER_LH" OR "OFFL_L2__CO____" OR "OFFL_L2__HCHO__" OR "OFFL_L2__NO2___" OR "OFFL_L2__NP_BD3" OR "OFFL_L2__NP_BD6" OR "OFFL_L2__NP_BD7" OR "OPER_AUX_CTMANA" OR "OPER_L0__ODB_4_" OR "OPER_L0__ODB_7_" OR "OPER_L0__PDQ___" OR "ZE_RAW__0S" OR "EW_RAW__0N" OR "IW_ETA__AX" OR "IW_RAW__0C" OR "S1_RAW__0A" OR "S1_RAW__0N" OR "S2_RAW__0N" OR "S4_RAW__0S" OR "S5_RAW__0C" OR "S5_RAW__0N" OR "WV_RAW__0N" OR "WV_RAW__0S" OR "Z1_RAW__0S" OR "Z7_RAW__0S" OR "DO_0_DOP___" OR "GN_0_GNS___" OR "MW_1_DNB_AX" OR "MW_1_NIR_AX" OR "OL_0_EFR___" OR "OL_1_RAC___" OR "OL_1_SPC___" OR "SL_1_VSC_AX" OR "SR_0_CAL___" OR "SR_1_CA1LAX" OR "SR_1_CA1SAX" OR "SR_1_CA2KAX" OR "AUX_BGHCHO" OR "AUX_BGSO2_" OR "AUX_L1_CKD" OR "AUX_O3_M" OR "NRTI_AUX_MET_QP" OR "NRTI_L1B_RA_BD7" OR "NRTI_L2__AER_AI" OR "NRTI_L2__AER_LH" OR "NRTI_L2__HCHO__" OR "NRTI_L2__NO2___" OR "NRTI_L2__O3____" OR "NRTI_L2__O3__PR" OR "NRTI_L2__SO2___" OR "OFFL_ICM_CA_UVN" OR "OFFL_L1B_CA_UVN" OR "OFFL_L1B_IR_SIR" OR "OFFL_L1B_RA_BD1" OR "OFFL_L1B_RA_BD3" OR "OFFL_L1B_RA_BD6" OR "OFFL_L1B_RA_BD7" OR "OFFL_L2__CLOUD_" OR "OFFL_L2__FRESCO" OR "OFFL_L2__O3____" OR "OFFL_L2__O3_TCL" OR "OFFL_L2__SO2___" OR "OPER_L0__ODB_2_" OR "OPER_L0__ODB_5_" OR "OPER_L0__ODB_6_" OR "OPER_L0__ODB_8_" OR "OPER_L0__SAT_A_" OR "AUX_O3PPWL" OR "MSI_L0__GR" OR "AUX_ML2" OR "AI_RAW__0_") AND nb_lta_served: [3 TO *]',
                        "refId": "LTA from PRIP",
                        "timeField": "sensing_start_date",
                        "datasourceId": 4,
                        "intervalMs": 86400000,
                        "maxDataPoints": 1,
                    },
                ],
                "from": "1743685310459",
                "to": "1743771710459",
            },
            "hideFromInspector": False,
        }
    }

    # Product type from dataflow to know what is expecte at DD/LTA from PRIP

    # Example of a dataflow report
    # {
    #   "product_type": "AUX_OBMEMC",
    #   "mission": "S1",
    #   "level": "AUX",
    #   "origin_level": "AUX",
    #   "instrument": "-",
    #   "mode": "-",
    #   "type": "-",
    #   "groups": [
    #     "AUX"
    #   ],
    #   "published_by": [
    #     "AUXIP",
    #     "_",
    #     "_",
    #     "_",
    #     "_"
    #   ],
    #   "consumed_by": [
    #     "AUXIP",
    #     "PRIP",
    #     "_",
    #     "_",
    #     "_"
    #   ],
    #   "reportName": "Copernicus_Ground_Segment_Sentinels_Data_Flow_Configuration_v1.2.csv",
    #   "ingestionTime": "2023-09-28T16:11:52.624Z",
    #   "reportFolder": "/files/MAAS/INBOX/DATAFLOW"
    # }

    dataflow_query = CdsDataflow.search().query(
        "bool",
        must=[
            {"term": {"published_by": "PRIP"}},
            {"term": {"consumed_by": "LTA"}},
            {"term": {"mission": "S1"}},
        ],
    )
    # didn't expect more than 10 0000 elements
    dataflow_documents = dataflow_query.params(size=1000).execute()

    # Next i think that the usage will be between two date
    start_date = "2025-01-01T00:00:00.000Z"
    end_date = "2025-01-02T00:00:00.000Z"

    # I query per satellite because some specific filter may be applied on specific mission, and it would be easy to manage these with this strategy

    datatake_query = CdsDatatake.search().query(
        "bool",
        must=[
            # {"term": {"mission": "S1"}}, #? choose if it is made per mission or satellite
            {"term": {"satellite_unit": "S1A"}},  # TODO make it dynamic
            {
                "range": {
                    "observation_time_start": {
                        "gte": start_date,
                        "lt": end_date,
                        # "format": "epoch_millis",
                    }
                }
            },
        ],
    )

    logger.debug(datatake_query.to_dict())

    target_product_type = [dataflow.product_type for dataflow in dataflow_documents]

    logger.info(f"Target product type: {len(target_product_type)} product_types")

    # Usage of scan() for request that expect more than 10 000 elements
    #! This is memory consuming
    target_datatake_id = [datatake.datatake_id for datatake in datatake_query.scan()]
    logger.info(f"Target datatake id: {len(target_datatake_id)} datatake_id")

    # Now we start to play with some complex request 😈

    #

    # Create a MultiSearch to perform a single request that contains multiple queries
    multi_search = MultiSearch()

    # Find element publish by prip
    product_query_prip = CdsProduct.search().query(
        "bool",
        must=[
            {"terms": {"datatake_id": target_datatake_id}},
            {"terms": {"product_type": target_product_type}},
            {"exists": {"field": "prip_id"}},  # Filter documents with a filled prip_id
        ],
    )
    product_query_prip.aggs.bucket(
        "datatake_id_terms", "terms", field="datatake_id", size=10
    )
    multi_search = multi_search.add(product_query_prip)

    # Find element publish by prip and by at least one LTA
    product_query_lta = CdsProduct.search().query(
        "bool",
        must=[
            {"terms": {"datatake_id": target_datatake_id}},
            {"terms": {"product_type": target_product_type}},
            {"exists": {"field": "prip_id"}},  # Filter documents with a filled prip_id
            {
                "range": {"nb_lta_served": {"gt": 1}}
            },  # Filter documents with nb_lta_served > 1
        ],
    )
    product_query_lta.aggs.bucket(
        "datatake_id_terms", "terms", field="datatake_id", size=10
    )
    multi_search = multi_search.add(product_query_lta)

    responses = multi_search.execute()

    # Response keep the order of search
    response_prip = responses[0]
    logger.info(
        f"Total matching products with prip_id: {response_prip.hits.total.value}"
    )
    for bucket in response_prip.aggregations.datatake_id_terms.buckets:
        logger.info(f"Datatake ID (prip): {bucket.key}, Count: {bucket.doc_count}")

    # Process the second response
    response_lta = responses[1]
    logger.info(
        f"Total matching products with nb_lta_served > 1: {response_lta.hits.total.value}"
    )
    for bucket in response_lta.aggregations.datatake_id_terms.buckets:
        logger.info(f"Datatake ID (lta): {bucket.key}, Count: {bucket.doc_count}")

    # Then we are able to display LTA Kpi for a bunch of datatake_id between two dates
