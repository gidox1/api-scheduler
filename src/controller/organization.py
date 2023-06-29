from src.service.organization.index import OrganizationService
from src.common import extract, Result
from flask import jsonify, request


class OrganizationController:
    def __init__(self, service: OrganizationService):
        self.service = service
        pass

    """
    Gets a single organization

    Args:
      org_id (str): The ID of the org being queried

    Returns:
      tuple: A tuple containing the JSON response and the HTTP status code.
  """

    def get(self, org_id, user_id):
        result = self.service.get(org_id, user_id)
        if Result.isError(result):
            return jsonify(result.error), 500
        return jsonify(result.value), 201

    """
    Creates a new Organization.

    Args:
      data (dict): A dictionary containing the organization's data.

    Returns:
      tuple: A tuple containing the JSON response and the HTTP status code.
  """

    def create(self, data):
        data = extract(
            data, [
                'name', 'country', 'city', 'address', 'owner_id'])
        result = self.service.create(data)
        if Result.isError(result):
            return jsonify(
                result.error), result.status if result.status is not None else 500
        return jsonify(result.value), 200

    """
    List Organizations based on pagination config

    Args:
      filters (dict): Pagination filter config

    Returns:
      tuple: A tuple containing the JSON response and the HTTP status code.
  """

    def listOrgs(self, filters):
        result = self.service.listOrgs(filters)
        if Result.isError(result):
            return jsonify(
                result.error), result.status if result.status is not None else 500
        return jsonify(result.value), 200

    """
    Delete an Organization

    Args:
      org_id (str): The Id of the organization to be deleted

    Returns:
      tuple: A tuple containing the JSON response and the HTTP status code.
  """

    def delete(self, org_id, user_id):
        result = self.service.delete(org_id, user_id)
        if Result.isError(result):
            return jsonify(
                result.error), result.status if result.status is not None else 500
        return jsonify(result.value), 200

    """
    Update an Organization

    Args:
      data (dict): The data to update on the organization
      user_id (str): The ID of the user performing the update

    Returns:
      tuple: A tuple containing the JSON response and the HTTP status code.
  """

    def update(self, data, user_id, org_id):
        result = self.service.update(data, user_id, org_id)
        if Result.isError(result):
          return jsonify(
              result.error), result.status if result.status is not None else 500
        return jsonify(result.value), 200
