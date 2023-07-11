from src.service.franchise import FranchiseService
from src.common import extract, Result
from flask import jsonify, request


class FranchiseController:
  def __init__(self, service: FranchiseService):
    self.service = service
    pass

  """
      Gets a single franchise by ID

      Args:
        id (str): The ID of the franchise being queried

      Returns:
        tuple: A tuple containing the JSON response and the HTTP status code.
    """

  def get(self, org_id, user_id):
    result = self.service.get(org_id, user_id)
    if Result.isError(result):
      return jsonify(result.error), 500
    return jsonify(result.value), 201

  """
    Creates a new Franchise for an organization.

    Args:
      data (dict): A dictionary containing the Franchise's data.

    Returns:
      tuple: A tuple containing the JSON response and the HTTP status code.
  """

  def create(self, data):
    data = extract(data,
                   ['name',
                    'country',
                    'address',
                    'manager_id',
                    'org_id',
                    'user_id',
                    'city',
                    'admin_details'])
    result = self.service.create(data)
    if Result.isError(result):
        return jsonify(
            result.error), result.status if result.status is not None else 500
    return jsonify(result.value), 200

  """
      List Franchise based on pagination config

      Args:
        filters (dict): Pagination filter config

      Returns:
        tuple: A tuple containing the JSON response and the HTTP status code.
    """

  def listFranchise(self, filters):
    result = self.service.listFranchise(filters)
    if Result.isError(result):
      return jsonify(
          result.error), result.status if result.status is not None else 500
    return jsonify(result.value), 200

  """
      Delete a Franchise

      Args:
        _id (str): The Id of the Franchise to be deleted

      Returns:
        tuple: A tuple containing the JSON response and the HTTP status code.
    """

  def delete(self, _id, user_id):
    result = self.service.delete(_id, user_id)
    if Result.isError(result):
      return jsonify(
          result.error), result.status if result.status is not None else 500
    return jsonify(result.value), 200

  """
      Update a Franchise

      Args:
        data (dict): The data to update on the franchise
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
