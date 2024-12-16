from enum import Enum
from typing import List


class TypesModel(Enum):
    SVD_TYPE = "svd"

class UtilsTypeModel:

    def get_list_types_model(self) -> List[str]:
        return [
            TypesModel.SVD_TYPE.value
        ]
