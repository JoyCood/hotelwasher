# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: member.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='member.proto',
  package='',
  syntax='proto2',
  serialized_pb=_b('\n\x0cmember.proto\"\xf2\x01\n\rMember_Washer\x12\n\n\x02id\x18\x01 \x02(\t\x12\x0c\n\x04nick\x18\x02 \x01(\t\x12\r\n\x05phone\x18\x03 \x01(\t\x12\x14\n\x0c\x61vatar_small\x18\x04 \x01(\t\x12\x12\n\navatar_mid\x18\x05 \x01(\t\x12\x12\n\navatar_big\x18\x06 \x01(\t\x12\r\n\x05level\x18\x07 \x01(\x02\x12\x10\n\x08reg_time\x18\x08 \x01(\x05\x12\x12\n\nlast_login\x18\t \x01(\x05\x12\x0e\n\x06status\x18\n \x01(\x05\x12\x10\n\x08\x64istance\x18\x0b \x01(\x02\x12\x11\n\tlongitude\x18\x0c \x01(\x02\x12\x10\n\x08latitude\x18\r \x01(\x02\"Q\n\rLogin_Request\x12\r\n\x05phone\x18\x01 \x02(\t\x12\x10\n\x08\x61uthcode\x18\x02 \x01(\x05\x12\x0c\n\x04uuid\x18\x03 \x02(\t\x12\x11\n\tsignature\x18\x04 \x01(\t\"e\n\x0eLogin_Response\x12\r\n\x05phone\x18\x01 \x01(\t\x12\x0e\n\x06secret\x18\x02 \x01(\t\x12\x0c\n\x04uuid\x18\x03 \x01(\t\x12&\n\nerror_code\x18\x04 \x02(\x0e\x32\x12.Member_Error_Code\")\n\x18Request_Authcode_Request\x12\r\n\x05phone\x18\x01 \x02(\t\"U\n\x19Request_Authcode_Response\x12\x10\n\x08\x61uthcode\x18\x01 \x01(\x05\x12&\n\nerror_code\x18\x02 \x02(\x0e\x32\x12.Member_Error_Code\"M\n\x13Near_Washer_Request\x12\x11\n\tcity_code\x18\x01 \x02(\x05\x12\x11\n\tlongitude\x18\x02 \x02(\x02\x12\x10\n\x08latitude\x18\x03 \x02(\x02\"^\n\x14Near_Washer_Response\x12\x1e\n\x06washer\x18\x01 \x03(\x0b\x32\x0e.Member_Washer\x12&\n\nerror_code\x18\x02 \x02(\x0e\x32\x12.Member_Error_Code*P\n\nHWProtocol\x12\x0e\n\nUNKNOW_CMD\x10\x00\x12\x0b\n\x05LOGIN\x10\xb0\xdb\x06\x12\x16\n\x10REQUEST_AUTHCODE\x10\xb1\xdb\x06\x12\r\n\x07KICKOUT\x10\xb2\xdb\x06*\xad\x01\n\x11Member_Error_Code\x12\x0b\n\x07SUCCESS\x10\x00\x12\x1c\n\x16\x45RROR_AUTHCODE_INVALID\x10\xb1\xdb\x06\x12\x19\n\x13\x45RROR_PHONE_INVALID\x10\xb2\xdb\x06\x12\x1c\n\x16\x45RROR_AUTHCODE_EXPIRED\x10\xb3\xdb\x06\x12\x1c\n\x16\x45RROR_MEMBER_NOT_FOUND\x10\xb4\xdb\x06\x12\x16\n\x10\x45RROR_BADREQUEST\x10\xb5\xdb\x06')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

_HWPROTOCOL = _descriptor.EnumDescriptor(
  name='HWProtocol',
  full_name='HWProtocol',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNKNOW_CMD', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LOGIN', index=1, number=110000,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REQUEST_AUTHCODE', index=2, number=110001,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='KICKOUT', index=3, number=110002,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=752,
  serialized_end=832,
)
_sym_db.RegisterEnumDescriptor(_HWPROTOCOL)

HWProtocol = enum_type_wrapper.EnumTypeWrapper(_HWPROTOCOL)
_MEMBER_ERROR_CODE = _descriptor.EnumDescriptor(
  name='Member_Error_Code',
  full_name='Member_Error_Code',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='SUCCESS', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERROR_AUTHCODE_INVALID', index=1, number=110001,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERROR_PHONE_INVALID', index=2, number=110002,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERROR_AUTHCODE_EXPIRED', index=3, number=110003,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERROR_MEMBER_NOT_FOUND', index=4, number=110004,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERROR_BADREQUEST', index=5, number=110005,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=835,
  serialized_end=1008,
)
_sym_db.RegisterEnumDescriptor(_MEMBER_ERROR_CODE)

Member_Error_Code = enum_type_wrapper.EnumTypeWrapper(_MEMBER_ERROR_CODE)
UNKNOW_CMD = 0
LOGIN = 110000
REQUEST_AUTHCODE = 110001
KICKOUT = 110002
SUCCESS = 0
ERROR_AUTHCODE_INVALID = 110001
ERROR_PHONE_INVALID = 110002
ERROR_AUTHCODE_EXPIRED = 110003
ERROR_MEMBER_NOT_FOUND = 110004
ERROR_BADREQUEST = 110005



_MEMBER_WASHER = _descriptor.Descriptor(
  name='Member_Washer',
  full_name='Member_Washer',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='Member_Washer.id', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='nick', full_name='Member_Washer.nick', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='phone', full_name='Member_Washer.phone', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='avatar_small', full_name='Member_Washer.avatar_small', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='avatar_mid', full_name='Member_Washer.avatar_mid', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='avatar_big', full_name='Member_Washer.avatar_big', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='level', full_name='Member_Washer.level', index=6,
      number=7, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='reg_time', full_name='Member_Washer.reg_time', index=7,
      number=8, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='last_login', full_name='Member_Washer.last_login', index=8,
      number=9, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='status', full_name='Member_Washer.status', index=9,
      number=10, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='distance', full_name='Member_Washer.distance', index=10,
      number=11, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='longitude', full_name='Member_Washer.longitude', index=11,
      number=12, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='latitude', full_name='Member_Washer.latitude', index=12,
      number=13, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=17,
  serialized_end=259,
)


_LOGIN_REQUEST = _descriptor.Descriptor(
  name='Login_Request',
  full_name='Login_Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='phone', full_name='Login_Request.phone', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='authcode', full_name='Login_Request.authcode', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='uuid', full_name='Login_Request.uuid', index=2,
      number=3, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='signature', full_name='Login_Request.signature', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=261,
  serialized_end=342,
)


_LOGIN_RESPONSE = _descriptor.Descriptor(
  name='Login_Response',
  full_name='Login_Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='phone', full_name='Login_Response.phone', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='secret', full_name='Login_Response.secret', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='uuid', full_name='Login_Response.uuid', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='error_code', full_name='Login_Response.error_code', index=3,
      number=4, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=344,
  serialized_end=445,
)


_REQUEST_AUTHCODE_REQUEST = _descriptor.Descriptor(
  name='Request_Authcode_Request',
  full_name='Request_Authcode_Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='phone', full_name='Request_Authcode_Request.phone', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=447,
  serialized_end=488,
)


_REQUEST_AUTHCODE_RESPONSE = _descriptor.Descriptor(
  name='Request_Authcode_Response',
  full_name='Request_Authcode_Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='authcode', full_name='Request_Authcode_Response.authcode', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='error_code', full_name='Request_Authcode_Response.error_code', index=1,
      number=2, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=490,
  serialized_end=575,
)


_NEAR_WASHER_REQUEST = _descriptor.Descriptor(
  name='Near_Washer_Request',
  full_name='Near_Washer_Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='city_code', full_name='Near_Washer_Request.city_code', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='longitude', full_name='Near_Washer_Request.longitude', index=1,
      number=2, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='latitude', full_name='Near_Washer_Request.latitude', index=2,
      number=3, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=577,
  serialized_end=654,
)


_NEAR_WASHER_RESPONSE = _descriptor.Descriptor(
  name='Near_Washer_Response',
  full_name='Near_Washer_Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='washer', full_name='Near_Washer_Response.washer', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='error_code', full_name='Near_Washer_Response.error_code', index=1,
      number=2, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=656,
  serialized_end=750,
)

_LOGIN_RESPONSE.fields_by_name['error_code'].enum_type = _MEMBER_ERROR_CODE
_REQUEST_AUTHCODE_RESPONSE.fields_by_name['error_code'].enum_type = _MEMBER_ERROR_CODE
_NEAR_WASHER_RESPONSE.fields_by_name['washer'].message_type = _MEMBER_WASHER
_NEAR_WASHER_RESPONSE.fields_by_name['error_code'].enum_type = _MEMBER_ERROR_CODE
DESCRIPTOR.message_types_by_name['Member_Washer'] = _MEMBER_WASHER
DESCRIPTOR.message_types_by_name['Login_Request'] = _LOGIN_REQUEST
DESCRIPTOR.message_types_by_name['Login_Response'] = _LOGIN_RESPONSE
DESCRIPTOR.message_types_by_name['Request_Authcode_Request'] = _REQUEST_AUTHCODE_REQUEST
DESCRIPTOR.message_types_by_name['Request_Authcode_Response'] = _REQUEST_AUTHCODE_RESPONSE
DESCRIPTOR.message_types_by_name['Near_Washer_Request'] = _NEAR_WASHER_REQUEST
DESCRIPTOR.message_types_by_name['Near_Washer_Response'] = _NEAR_WASHER_RESPONSE
DESCRIPTOR.enum_types_by_name['HWProtocol'] = _HWPROTOCOL
DESCRIPTOR.enum_types_by_name['Member_Error_Code'] = _MEMBER_ERROR_CODE

Member_Washer = _reflection.GeneratedProtocolMessageType('Member_Washer', (_message.Message,), dict(
  DESCRIPTOR = _MEMBER_WASHER,
  __module__ = 'member_pb2'
  # @@protoc_insertion_point(class_scope:Member_Washer)
  ))
_sym_db.RegisterMessage(Member_Washer)

Login_Request = _reflection.GeneratedProtocolMessageType('Login_Request', (_message.Message,), dict(
  DESCRIPTOR = _LOGIN_REQUEST,
  __module__ = 'member_pb2'
  # @@protoc_insertion_point(class_scope:Login_Request)
  ))
_sym_db.RegisterMessage(Login_Request)

Login_Response = _reflection.GeneratedProtocolMessageType('Login_Response', (_message.Message,), dict(
  DESCRIPTOR = _LOGIN_RESPONSE,
  __module__ = 'member_pb2'
  # @@protoc_insertion_point(class_scope:Login_Response)
  ))
_sym_db.RegisterMessage(Login_Response)

Request_Authcode_Request = _reflection.GeneratedProtocolMessageType('Request_Authcode_Request', (_message.Message,), dict(
  DESCRIPTOR = _REQUEST_AUTHCODE_REQUEST,
  __module__ = 'member_pb2'
  # @@protoc_insertion_point(class_scope:Request_Authcode_Request)
  ))
_sym_db.RegisterMessage(Request_Authcode_Request)

Request_Authcode_Response = _reflection.GeneratedProtocolMessageType('Request_Authcode_Response', (_message.Message,), dict(
  DESCRIPTOR = _REQUEST_AUTHCODE_RESPONSE,
  __module__ = 'member_pb2'
  # @@protoc_insertion_point(class_scope:Request_Authcode_Response)
  ))
_sym_db.RegisterMessage(Request_Authcode_Response)

Near_Washer_Request = _reflection.GeneratedProtocolMessageType('Near_Washer_Request', (_message.Message,), dict(
  DESCRIPTOR = _NEAR_WASHER_REQUEST,
  __module__ = 'member_pb2'
  # @@protoc_insertion_point(class_scope:Near_Washer_Request)
  ))
_sym_db.RegisterMessage(Near_Washer_Request)

Near_Washer_Response = _reflection.GeneratedProtocolMessageType('Near_Washer_Response', (_message.Message,), dict(
  DESCRIPTOR = _NEAR_WASHER_RESPONSE,
  __module__ = 'member_pb2'
  # @@protoc_insertion_point(class_scope:Near_Washer_Response)
  ))
_sym_db.RegisterMessage(Near_Washer_Response)


# @@protoc_insertion_point(module_scope)
