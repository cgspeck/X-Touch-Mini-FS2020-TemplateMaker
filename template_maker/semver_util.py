from typing import Mapping, Union
from semver import VersionInfo
import yaml
from yaml import Loader
from yaml import FullLoader
from yaml import UnsafeLoader


def version_info_representer(dumper: yaml.dumper.Dumper, data: VersionInfo):
    return dumper.represent_scalar("VersionInfo", str(data))


def version_info_constructor(
    loader: Union[Loader, FullLoader, UnsafeLoader], node: yaml.Node
):
    value: str = loader.construct_scalar(node)  # type: ignore
    return VersionInfo.parse(value)


def extend_yaml_lib():
    yaml.add_representer(VersionInfo, version_info_representer)
    yaml.add_constructor("VersionInfo", version_info_constructor)
