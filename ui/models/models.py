from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Server:
    name: str
    ip: str
    port: int
    login: str
    password: str
    is_swarm: bool
    is_master_node: bool
    swarm_parent: Optional[str]
    install_nginx: bool


@dataclass
class Application:
    name: str
    local_path: str
    dest_path: str
    environments: Optional[List[str]]
    # environment_dir: str
    is_swarm: bool
    server: str

@dataclass
class Registry:
    name: str
    url: Optional[str]
    login: str
    password: str

@dataclass
class Domain:
    name: str
    port: int
    # config_path: str
    is_ssl: bool
    server: str
