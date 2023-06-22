from src.model.user import User
import enum

def map_user_data(user: User):
  user_dict = convert_to_dict(user)
  del user_dict['password']
  return user_dict

def convert_to_dict(model):
    model_dict = {}
    for column in model.__table__.columns:
        attribute_name = column.name
        attribute_value = getattr(model, attribute_name)

        # Convert enum values to string representation
        if isinstance(attribute_value, enum.Enum):
            attribute_value = attribute_value.value

        model_dict[attribute_name] = attribute_value
    return model_dict