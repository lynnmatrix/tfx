# Copyright 2019 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Base class for TFX components."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import abc

from six import with_metaclass

from typing import Dict, List, Text, Tuple

from tfx import types
from tfx.orchestration import metadata


class ResolveResult(object):
  """The data structure to hold results from Resolver.

  Attributes:
    per_key_resolve_result: a key -> Tuple[List[Artifact], bool] dict containing
      the artifact resolution result and a bool value indicating whether the
      resolved result is complete.
    has_complete_result: bool value indicating whether all desired artifacts
      have been resolved.
  """

  def __init__(self, per_key_resolve_result: Dict[Text,
                                                  Tuple[List[types.Artifact],
                                                        bool]]):
    self.per_key_resolve_result = per_key_resolve_result
    self.has_complete_result = all(
        [t[1] for t in per_key_resolve_result.values()])


class BaseResolver(with_metaclass(abc.ABCMeta, object)):
  """Base class for resolver.

  Resolver is the logical unit that will be used optionally for input selection.
  A resolver subclass must override the resolve() function which takes a
  read-only MLMD handler and a dict of <key, Channel> as parameters and produces
  a ResolveResult instance.
  """

  @abc.abstractmethod
  def resolve(
      self,
      metadata_handler: metadata.Metadata,
      source_channels: Dict[Text, types.Channel],
  ) -> ResolveResult:
    """Resolves artifacts from channels by querying MLMD.

    Args:
      metadata_handler: a read-only handler to query MLMD.
      source_channels: a key -> channel dict which contains the info of the
        source channels.

    Returns:
      a ResolveResult instance.

    """
    raise NotImplementedError