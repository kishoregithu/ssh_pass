#tsr_api.py
def post_export_tsr_report(self, user=CURRENT_USER, domain=NUANCE_DOMAIN, file_name, file_format, show_detail_by_did, show_transfer_duration_info):
    """
    API - Export the Telephony Summary Report based on user’s selection in various file formats
    :param user: logged in user
    :param domain: current domain 
    :param file_format: file format (csv, xml, pdf)
    :param file_name: full path of the file
    :param show_detail_by_did: Show Detail by DID
    :param show_transfer_duration_info: Show transfer duration information
    return: API Response
    """
    url = self.util.build_https_url(os.path.join(const.TSR_MANAGER_URL, 'export')).replace("\\", "/")
    headers = sel.get_header(user)
    params = {}
    if domain is not None:
        domain = domain if domain != const.NULL else None
        params.update({'domain':domain})
    response = self.util.send_request(const.GET, url, params=params, headers=headers)
    return response

tsr_helper
def build_export_tsr_usage_report_payload(org_id=BVPAYS_ORGID, app_ids=NUANCE_APP_ID, called_parties=CALLED_PARTY_LIST,
                                          call_type=INBOUND_CALL_TYPE, wrc_billable=WCR_BILL_FALSE, start_date=TEST_START_DATE, end_date=TEST_END_DATE, time_zone=TIME_ZONE_PACEFIC):
    
    return data
    
#test_user_controller.py
@pytest.mark.parametrize("file_format",[(CSV_FORMAT), (XML_FORMAT), (PDF_FORMAT) ])
def test_export_valid_tsr_report_file(self,file_format):
    """
    This Test Varifies:
    1. Export TSR by giving all valid details and format as CSV.
    2. Export TSR by giving all valid details and format as XML.
    3. Export TSR by giving all valid details and format as PDF.
    """
    data = self.build_export_tsr_usage_report_payload()
    file = RANDOM_FILE_NAME
    response = self.post_export_tsr_report(data, file, file_format)
    assert HTTP_OK ==  response.status
    
    
    

    
