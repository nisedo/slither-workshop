import collections
from typing import Dict, List
from slither.core.declarations import FunctionContract
from slither.printers.abstract_printer import AbstractPrinter
from slither.utils import output
from slither.utils.colors import blue, green, red
from slither.utils.output import Output

class EntryPoints(AbstractPrinter):
    ARGUMENT = "entry-points"
    HELP = "Print the entry points of the codebase"

    WIKI = "https://github.com/trailofbits/slither/wiki/Printer-documentation#TBD"

    def output(self, _filename: str) -> Output:

        txt = ""  # Initialize an empty string to store the output

        all_contracts = []  # Initialize an empty list to store all contracts

        # Loop through each contract
        for contract in self.contracts:

            # Check if the contract is upgradeable or a proxy
            is_upgradeable_proxy = contract.is_upgradeable_proxy
            is_upgradeable = contract.is_upgradeable

            additional_txt_info = ""  # Initialize an empty string to store additional info

            # Add additional info based on the contract properties
            if is_upgradeable_proxy:
                additional_txt_info += " (Upgradeable Proxy)"

            if is_upgradeable:
                additional_txt_info += " (Upgradeable)"

            if contract in self.slither.contracts_derived:
                additional_txt_info += " (Most derived contract)"

            # Create an Output object with additional fields
            additional_fields = output.Output(
                "",
                additional_fields={
                    "is_upgradeable_proxy": is_upgradeable_proxy,
                    "is_upgradeable": is_upgradeable,
                    "is_most_derived": contract in self.slither.contracts_derived,
                },
            )

            # Get all public functions of the contract
            public_function = [
                (f.contract_declarer.name, f)
                for f in contract.functions
                if (not f.is_shadowed and not f.is_constructor_variables)
            ]

            # Group the functions by the contract declarer
            collect: Dict[str, List[FunctionContract]] = collections.defaultdict(list)
            for a, b in public_function:
                collect[a].append(b)

            # Initialize a flag to check if any function is printed for the contract
            is_function_printed = False

            # Skip if the contract is an interface or a library
            if contract.is_interface or contract.is_library:
                continue

            # Loop through each contract and its functions
            for contract, functions in collect.items():
                # Filter functions based on entry points criteria
                filtered_functions = [
                    function for function in functions
                    if function.visibility in ["external", "public"] and not function.view and not function.pure and not function.is_empty and not function.is_constructor
                ]

                # Only proceed if there are any functions that meet the criteria
                if filtered_functions:
                    if not is_function_printed:
                        txt += blue(f"\n+ Contract {contract.name}{additional_txt_info}\n")
                        is_function_printed = True

                    txt += blue(f"  - From {contract}\n")

                    # Sort functions by the joined string of modifiers, then by the function name
                    filtered_functions = sorted(filtered_functions, key=lambda f: (' - '.join(str(modifier) for modifier in f.modifiers), f.full_name))

                    # Loop through each function
                    for function in filtered_functions:
                        # Create a list of modifiers
                        modifiers = [str(modifier) for modifier in function.modifiers]

                        # Only add the modifiers to the function string if there are any
                        if modifiers:
                            txt += red(f"    - {function.full_name}") + " " + green(' '.join(modifiers)) + "\n"
                        else:
                            txt += red(f"    - {function.full_name}\n")

                    # Add the function visibility to the output if it's not one of the standard visibilities
                    if function.visibility not in [
                        "external",
                        "public",
                        "internal",
                        "private",
                    ]:
                        txt += f"    - {function.full_name}  ({function.visibility})\n"

                    # Add the function and its visibility to the additional fields
                    additional_fields.add(
                        function, additional_fields={"visibility": function.visibility}
                    )

            # Add the contract and its additional fields to the list of all contracts
            all_contracts.append((contract, additional_fields.data))

        # Print the output
        self.info(txt)

        # Generate the final output
        results = self.generate_output(txt)
        for current_contract, current_additional_fields in all_contracts:
            results.add(current_contract, additional_fields=current_additional_fields)

        # Return the final output
        return results

# slither /Users/nisedo/Documents/audit/2024-06-size/ --print entry-points
