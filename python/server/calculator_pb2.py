# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: calculator.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'calculator.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10\x63\x61lculator.proto\x12\ncalculator\"j\n\x0f\x42inaryOperation\x12\x15\n\rfirst_operand\x18\x01 \x01(\x02\x12\x16\n\x0esecond_operand\x18\x02 \x01(\x02\x12(\n\toperation\x18\x03 \x01(\x0e\x32\x15.calculator.Operation\"#\n\x11\x43\x61lculationResult\x12\x0e\n\x06result\x18\x01 \x01(\x02*\"\n\tOperation\x12\x07\n\x03\x41\x44\x44\x10\x00\x12\x0c\n\x08SUBTRACT\x10\x01\x32U\n\nCalculator\x12G\n\tCalculate\x12\x1b.calculator.BinaryOperation\x1a\x1d.calculator.CalculationResultb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'calculator_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_OPERATION']._serialized_start=177
  _globals['_OPERATION']._serialized_end=211
  _globals['_BINARYOPERATION']._serialized_start=32
  _globals['_BINARYOPERATION']._serialized_end=138
  _globals['_CALCULATIONRESULT']._serialized_start=140
  _globals['_CALCULATIONRESULT']._serialized_end=175
  _globals['_CALCULATOR']._serialized_start=213
  _globals['_CALCULATOR']._serialized_end=298
# @@protoc_insertion_point(module_scope)
