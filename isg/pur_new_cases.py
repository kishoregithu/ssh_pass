@pytest.mark.parametrize("startTime", "endTime" ,[(START_TIME_LONG, END_TIME_LONG), (END_TIME_LONG, START_TIME_LONG)])
def test_port_usage_export_with_long_timeperiod(self,startTime, endTime):
    """
    This test verified 
    1. the port usage export with long time period than 30 days
    2. the port usage export with long time period with start time is less than end time
    """
    data = self.build_export_port_usage_report_payload(startTime,endTime)
    file = RANDOM_FILE_NAME
    response = self.get_export_port_usage_apt(data, file)
    assert HTTP_OK ==  response.status
    
@pytest.mark.parametrize("app_id" ,[(INVALID_APP_ID)])
def test_port_usage_export_with_app_id_not_in_org(self,startTime, endTime):
    """
    This test verified the port usage export with app_id does not belog to orgid
    """
    data = self.build_export_port_usage_report_payload(app_id)
    file = RANDOM_FILE_NAME
    response = self.get_export_port_usage_apt(data, file)
    assert HTTP_OK ==  response.status 
    
@pytest.mark.parametrize("org_id" ,[(INVALID_ORG_ID)])
def test_port_usage_export_with_org_id_not_in_domain(self,startTime, endTime):
    """
    This test verified the port usage export with org_id does not belog to domain
    """
    data = self.build_export_port_usage_report_payload(org_id)
    file = RANDOM_FILE_NAME
    response = self.get_export_port_usage_apt(data, file)
    assert HTTP_OK ==  response.status 
    

def test_port_usage_export_with_file_contain_no_data(self,startTime, endTime):
    """
    This test verified the port usage export with file contain no data
    """
    data = self.build_export_port_usage_report_payload(org_id)
    file = NO_DATA_FILE_NAME
    response = self.get_export_port_usage_apt(data, file)
    assert HTTP_OK ==  response.status 
