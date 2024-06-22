from typing import List
from slither.detectors.abstract_detector import (
    AbstractDetector,
    DetectorClassification,
    DETECTOR_INFO,
)
from slither.utils.output import Output

class IsContract(AbstractDetector):
    """
    <Documentation>
    """

    ARGUMENT = "iscontract" 
    HELP = "IsContract is misused"
    IMPACT = DetectorClassification.MEDIUM
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = "https://github.com/crytic/slither/wiki/Adding-a-new-detector"
    WIKI_TITLE = "Example"
    WIKI_DESCRIPTION = "Plugin example"
    WIKI_EXPLOIT_SCENARIO = ".."
    WIKI_RECOMMENDATION = ".."

    def _detect(self) -> List[Output]:
        # Initialize an empty list to store the results of the detection
        results: List[Output] = []
        # Iterate over each contract derived in the compilation unit
        for contract in self.contracts:
            # Iterate over each modifier defined in the contract
            for modifier in contract.modifiers:
                # Check if the modifier's name is "isContract"
                if modifier.name == "isContract":
                    # Check if the modifier contains inline assembly code
                    if modifier.contains_assembly:
                        # Iterate over each node in the modifier's control flow
                        for node in modifier.nodes:
                            # Check if the node contains a specific assembly call to "extcodesize"
                            if "extcodesize(uint256)" in str(node.expression):
                                # Prepare the information about the issue to be reported
                                info: DETECTOR_INFO = [
                                    "contract ", contract.name, 
                                    " contains an incorrect call to extcodesize: ", node, "\n"
                                ]
                                # Append the result to the results list using the generated information
                                results.append(self.generate_result(info))
        # Return the list of results collected during the detection process
        return results

# slither evaluation/iscontract/example.sol --detect iscontract --solc-disable-warnings 