from enum import Enum


class Target(Enum):

    PAYS = 0xb0
    FIN_TACHE = 0xb4
    STM_COMMANDS = {PAYS, FIN_TACHE}
