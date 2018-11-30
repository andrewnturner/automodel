class Field:
    def build_from_data(self, data):
        raise NotImplementedError

    def make_for_dict(self, data):
        raise NotImplementedError


class StringField(Field):
    def build_from_data(self, data):
        return data

    def make_for_dict(self, data):
        return data


class ModelField(Field):
    def __init__(self, model_cls):
        self.model_cls = model_cls

    def build_from_data(self, data):
        return self.model_cls.from_dict(data)

    def make_for_dict(self, data):
        return data.as_dict()


class ModelMeta(type):
    def __new__(cls, cls_name, bases, attrs):
        fields = {
            name: value for name, value in attrs.items() if isinstance(value, Field)
        }
        for name in fields.keys():
            del attrs[name]

        def cls__init__(self, *args, **kwargs):
            for name, arg in zip(fields.keys(), args):
                setattr(self, name, arg)
        attrs["__init__"] = cls__init__

        @classmethod
        def from_dict(inner_cls, data):
            args = []
            for name, field in fields.items():
                field_data = data[name]
                args.append(field.build_from_data(field_data))
            return inner_cls(*args)
        attrs["from_dict"] = from_dict

        def as_dict(self):
            return {
                name: field.make_for_dict(getattr(self, name))
                for name, field in fields.items()
            }
        attrs["as_dict"] = as_dict

        return super(ModelMeta, cls).__new__(cls, cls_name, bases, attrs)

class Model(metaclass=ModelMeta):
    pass
