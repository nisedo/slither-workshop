from typing import List
from slither.detectors.abstract_detector import (
    AbstractDetector,
    DetectorClassification,
    DETECTOR_INFO,
)
from slither.utils.output import Output
from slither.slithir.operations import Binary, BinaryType

class DivideByTotalSupply(AbstractDetector):
    """
    <Documentation>
    """

    ARGUMENT = "divide-by-total-supply" 
    HELP = "Divide by total suppy"
    IMPACT = DetectorClassification.HIGH
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = "https://github.com/crytic/slither/wiki/Adding-a-new-detector"
    WIKI_TITLE = "Example"
    WIKI_DESCRIPTION = "Plugin example"
    WIKI_EXPLOIT_SCENARIO = ".."
    WIKI_RECOMMENDATION = ".."

    def _detect(self) -> List[Output]:
        # Initialize an empty list to store the results
        results: List[Output] = []

        # Iterate over all derived contracts in the compilation unit
        for contract in self.compilation_unit.contracts_derived:
            # Iterate over all functions in the contract
            for function in contract.functions:
                # Iterate over all nodes in the function
                for node in function.nodes:
                    # Iterate over all intermediate representations (IRs) in the node
                    for ir in node.irs:
                        # Check if the IR is a binary operation
                        if isinstance(ir, Binary):
                            # Check if the binary operation is a division
                            if ir.type == BinaryType.DIVISION:
                                # Check if the division involves total supply
                                if "/ totalSupply()" in str(ir.expression) or "/ total_supply" in str(ir.expression):
                                    # Create an info message with details about the contract and node
                                    info: DETECTOR_INFO = [
                                        "contract ", contract.name, 
                                        " contains a division by total supply: ", node, "\n"
                                    ]
                                    # Append the generated result to the results list
                                    results.append(self.generate_result(info))
        # Return the list of results
        return results
    
# slither evaluation/divide_by_total_supply/example.sol --detect divide-by-total-supply --solc-disable-warnings