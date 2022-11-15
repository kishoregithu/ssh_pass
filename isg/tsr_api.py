#tsr_api.py
def post_export_tsr_report(self, user, domain, format, file_name, show_detail_by_did, show_transfer_duration_info):
    """
    API - Export the Telephony Summary Report based on user’s selection in various file formats
    :param user: logged in user
    :param domain: current domain 
    :param format: file format (csv, xml, pdf)
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


#test_user_controller.py
@pytest.mark.parametrize("domain, user, role",[(NUANCE_DOMAIN, DAC_OPERATOR, ROLE_OPERATOR),
                                               (NUANCE_DOMAIN, DAC_ADMIN, ROLE_ADMIN) ])
def test_get_user_priviliages_for_app(self,domain, user):
    """
    This test verified the priviliages of an user for an app
    """
    response = self.get_tsr_user_priv_for_app(domain, user, DAC)
    response_json = json.loads(response.text)
    assert HTTP_OK ==  response.status
    assert role == response_json [0]["applicationRoles"][0]
    assert "DAC" ==  response_json [0]['applicationName']
    
    
def test_get_user_priviliages_for_app_role(self,domain, user):
    """
    This test verified the priviliages of an user for an app role
    """
    response = self.get_tsr_user_priv_for_app(NUANCE_DOMAIN, DAC_OPERATOR, NCP)
    response_json = json.loads(response.text)
    assert HTTP_OK ==  response.status
    assert "NCP" ==  response_json [0]['applicationName']
    assert "ROLE_NCP_FRONTEND" ==  response_json [0]['applicationRole']
    
@pytest.mark.parametrize("domain, user, role, app ",[(NUANCE_DOMAIN, COM_OPERATOR, ROLE_OPERATOR, COM),
                                               (NUANCE_DOMAIN, COM_ADMIN, ROLE_ADMIN, COM),
                                               (NUANCE_DOMAIN, COM_VIEWER, ROLE_VIEWER, COM),
                                               (NUANCE_DOMAIN, COM_ADMIN, ROLE_ADMIN, PUR),
                                               (NUANCE_DOMAIN, COM_OPERATOR, ROLE_VIEWER, PUR),
                                              ])
def test_get_user_priviliages_for_app_access(self,domain, user):
    """
    This test verified the priviliages of an user for an app with access
    """
    response = self.get_tsr_user_priv_for_app(domain, user, app)
    response_json = json.loads(response.text)
    assert HTTP_OK ==  response.status
    assert app ==  response_json [0]['applicationName']
    assert role == assert "Administrator" == response_json [0]["applicationRoles"][0]
    
@pytest.mark.parametrize("domain, user, app ",[(NUANCE_DOMAIN, APP_OPERATOR, AM),
                                               (NUANCE_DOMAIN, APP_ADMIN, AM),
                                              ])
def test_get_user_priviliages_for_app_access_negative(self,domain, user):
    """
    This test verified the priviliages of an user for an app with no access
    """
    response = self.get_tsr_user_priv_for_app(domain, user, app)
    response_json = json.loads(response.text)
    assert HTTP_FORBIDDEN ==  response.status
    assert app ==  response_json [0]['applicationName']
    
@pytest.mark.parametrize("domain, user, role, app ",[(NUANCE_DOMAIN, LOG_OPERATOR, ROLE_OPERATOR, LV),
                                               (NUANCE_DOMAIN, LOG_ADMIN, ROLE_ADMIN, LV),
                                               (NUANCE_DOMAIN, TSR_OPERATOR, ROLE_OPERATOR, TSR),
                                               (NUANCE_DOMAIN, TSR_ADMIN, ROLE_ADMIN, TSR)
                                              ])
def test_get_user_priviliages_for_app_no_access(self,domain, user):
    """
    This test verified the priviliages of an user for an app with no access
    """
    response = self.get_tsr_user_priv_for_app(domain, user, app)
    response_json = json.loads(response.text)
    assert HTTP_OK ==  response.status
    assert app ==  response_json [0]['applicationName']
    assert role == assert "Administrator" == response_json [0]["applicationRoles"][0]
    
def test_get_user_priviliages_for_app_invalid_domain(self):
    """
    This test verified the priviliages of an user for an app with invalid domain
    """
    response = self.get_tsr_user_priv_for_app(const.NULL, DAC_ADMIN, DAC)
    assert HTTP_FORBIDDEN ==  response.status
    response = self.get_tsr_user_priv_for_app('', DAC_ADMIN, DAC)
    assert HTTP_FORBIDDEN ==  response.status
    response = self.get_tsr_user_priv_for_app('abcd', DAC_ADMIN, DAC)
    assert HTTP_FORBIDDEN ==  response.status
    response = self.get_tsr_user_priv_for_app(None, DAC_ADMIN, DAC)
    assert HTTP_FORBIDDEN ==  response.status
    
