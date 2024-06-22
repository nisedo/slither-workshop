from typing import List

from slither.detectors.abstract_detector import (
    AbstractDetector,
    DetectorClassification,
    DETECTOR_INFO,
)
from slither.utils.output import Output


class UnusedEvent(AbstractDetector):
    """
    <Documentation>
    """

    ARGUMENT = "unused-event" 
    HELP = "Unused event"
    IMPACT = DetectorClassification.OPTIMIZATION
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
        for contract in self.compilation_unit.contracts_derived:
            # Iterate over each event defined in the contract
            for event in contract.events:
                # Iterate over each function called in the contract
                for function in contract.all_functions_called:
                    # Iterate over each node in the function's control flow
                    for node in function.nodes:
                        # Iterate over each intermediate representation (IR) in the node
                        for ir in node.irs:
                            # Check if the IR does not correspond to the event
                            if str(ir).split('(')[0].replace("Emit ", "") != str(event):
                                # Prepare the information about the unused event to be reported
                                info: DETECTOR_INFO = [
                                    "contract ", contract.name, 
                                    " contains an unused event: ", event, "\n"
                                ]
                                # Append the result to the results list using the generated information
                                results.append(self.generate_result(info))
        # Return the list of results collected during the detection process
        return results

# slither evaluation/unused_event/example.sol --detect unused-event --solc-disable-warnings