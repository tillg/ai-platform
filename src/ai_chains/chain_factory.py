import json
from typing import Any, Dict, List
from ai_chains.chain import Chain
from ai_commons.constants import CHAINS_INDEX_FILE
import os
import logging
from utils.dict2file import write_dict_to_file, read_dict_from_file

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

CHAIN_TYPES = ["default", "simple_rag", "naked_llm"]


class ChainFactory:
    chains_index = {}

    def __init__(self, chains_index_file: str = CHAINS_INDEX_FILE):
        if not os.path.exists(chains_index_file):
            logger.warning(f"Chains index file not found: {chains_index_file}, using default chains.")
            self.chains_index = self._create_default_chains_index()
        else:
            self.chains_index = read_dict_from_file(full_filename=chains_index_file)
        logger.info(f"Chains index before setting default: {self.chains_index}")
        # If we have a default_chain name in the index file, we need to copy over the parameters of that chain into the §default_chain"
        if "default_chain" in self.chains_index.keys():
            default_chain_id = self.chains_index["default_chain"]
            if default_chain_id not in self.chains_index:
                raise ValueError(f"Default chain ID {default_chain_id} not found in chains index.")
            else:
                self.chains_index["default_chain"] = self.chains_index[default_chain_id]
        else:
            # No default_chain was specified, so we just use the 1st one as default
            self.chains_index["default_chain"] = self.chains_index[next(iter(self.chains_index))]
        logger.info(f"__init__: Chains index: {self.chains_index}")

    def _create_default_chains_index(self):
        chains_index = {}
        for chain_type in CHAIN_TYPES:
            chains_index[chain_type] = {
                'chain_type': chain_type
            }
        return chains_index

    def is_valid_chain_id(self, chain_id: str) -> bool:
        return chain_id in self.chains_index.keys()
    
    def get_chain_list(self) -> List[str]:
        return self.chains_index.keys()

    def create_chain(self, parameters: Dict[str, Any]) -> Chain:
        logger.info(f"Creating chain with parameters: {parameters}")
        chain_type = parameters.get('chain_type', 'default')
        logger.info(f"Creating chain with parameters (after setting default chain type): {parameters}")
        if chain_type == 'default':
            from ai_chains.chains.default.chain import Chain
            return Chain(parameters)
        elif chain_type == 'simple_rag':
            from ai_chains.chains.simple_rag.chain import Chain
            return Chain(parameters)
        elif chain_type == 'naked_llm':
            from ai_chains.chains.naked_llm.chain import Chain
            return Chain(parameters)
        else:
            raise ValueError(f"Invalid chain type: {chain_type}")

    
    def create_chain_by_id(self, chain_id: str) -> Chain:
        if not self.is_valid_chain_id(chain_id):
            raise ValueError(f"Invalid chain ID: {chain_id}")
        chain_parameters = self.chains_index[chain_id]
        logger.info(f"Creating chain with parameters: {chain_parameters} taken from index {json.dumps(self.chains_index, indent=2)}")
        chain = self.create_chain(chain_parameters)
        chain.parameters['id'] = chain_id
        return chain