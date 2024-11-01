from wrike.core.constants import (
    WRIKE_BASE_URL
)


def update_contact(contact_id, metadata=None, custom_fields=None, current_bill_rate=None, current_cost_rate=None,
                         job_role_id=None, verbose=False):
    """
    Updates a contact's metadata, custom fields, and other optional details in Wrike. The contact_id is required to
    identify the contact. Metadata, custom fields, and other fields like bill rate or cost rate are optional.

    Constructs a PUT request to the '/contacts/{contactId}' endpoint, where contact_id is the ID of the contact to be updated.

    metadata list of dicts, as follows:

        [{'key': 'testMetaKey', 'value': 'testMetaValue'}]      todo: real example

    custom_fields list of dicts, as follows:

        [{'id': 'customFieldId', 'value': 'desired_value'}]     todo: real example

    current_bill_rate dict should have fields such as 'rateScope', 'rateSource', and 'rateValue', as follows:

        todo: real example

    current_cost_rate should have fields such as 'rateScope', 'rateSource', and 'rateValue', as follows:

    Returns a JSON containing updated contact details, if successful, as follows:

        todo: real example

    :param contact_id:          str, required           ID of contact to update
    :param metadata:            list, optional          list of dicts containing metadata to update
    :param custom_fields:       list, optional          list of dicts containing custom field updates
    :param current_bill_rate:   dict, optional          dict of user's bill rate
    :param current_cost_rate:   dict, optional          dict of user's cost rate
    :param job_role_id:         str, optional           ID of user's job role
    :param verbose:             bool, optional          if True, print status to terminal
    :return:                    JSON                    JSON containing updated contact details
    """

    update_contact_url = WRIKE_BASE_URL + f'/contacts/{contact_id}'
    print(update_contact_url) if verbose else None

    payload = {}

    if metadata:
        payload['metadata'] = metadata
    if custom_fields:
        payload['customFields'] = custom_fields
    if current_bill_rate:
        payload['currentBillRate'] = current_bill_rate
    if current_cost_rate:
        payload['currentCostRate'] = current_cost_rate
    if job_role_id:
        payload['jobRoleId'] = job_role_id

    if not payload:
        raise ValueError('No valid fields provided for update. You must provide at least one updatable field.')

    return update_contact_url, payload, verbose
