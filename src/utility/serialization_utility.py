import datetime
import inspect
import json
from typing import final, Any

import pydantic
from loguru import logger


@final
class SerializationUtility:

    @staticmethod
    def shoud_be_serializeable(member: tuple[str, Any]) -> bool:
        key, value = member
        return not key.startswith("_") and \
            not key[0].isupper() and \
            not inspect.isclass(value) and \
            not inspect.isroutine(value) and \
            not inspect.ismodule(value)

    @staticmethod
    def serialize(obj: Any, seen: list = None) -> Any:
        if isinstance(obj, (int, float, str, bool)) or obj is None:
            return obj
        if isinstance(obj, bytes):
            return repr(obj)
        if isinstance(obj, dict):
            return {str(k): SerializationUtility.serialize(v, seen) for k, v in obj.items()}
        if isinstance(obj, (list, tuple, set, frozenset)):
            return [SerializationUtility.serialize(x, seen) for x in obj]

        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        if isinstance(obj, pydantic.BaseModel):
            return {k: SerializationUtility.serialize(v, seen) for k, v in obj.model_dump().items()}

        if seen is None:
            seen = [obj]
        elif obj in seen:
            return repr(obj)
        else:
            seen.append(obj)

        # if obj is some sctructure
        members = filter(SerializationUtility.shoud_be_serializeable, inspect.getmembers(obj))
        return {k: SerializationUtility.serialize(v, seen) for k, v in members}

    @staticmethod
    def to_json(obj: Any) -> str:
        return json.dumps(SerializationUtility.serialize(obj), sort_keys=True)

    @staticmethod
    def try_to_json(obj: Any) -> str:
        try:
            return SerializationUtility.to_json(obj)
        except Exception as e:
            logger.error("Serialization failed: {}", e)
            return repr(obj)
