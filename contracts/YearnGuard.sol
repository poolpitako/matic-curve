// SPDX-License-Identifier: AGPL-3.0

pragma solidity 0.6.12;
pragma experimental ABIEncoderV2;

import "@openzeppelin/contracts/utils/EnumerableSet.sol";

contract Enum {
    enum Operation {Call, DelegateCall}
}

interface GnosisSafe {
    function getOwners() external view returns (address[] memory);
}

interface Guard {
    function checkTransaction(
        address to,
        uint256 value,
        bytes memory data,
        Enum.Operation operation,
        uint256 safeTxGas,
        uint256 baseGas,
        uint256 gasPrice,
        address gasToken,
        address payable refundReceiver,
        bytes memory signatures,
        address msgSender
    ) external;
}

contract YearnGuard is Guard {
    using EnumerableSet for EnumerableSet.AddressSet;

    GnosisSafe public safe;
    EnumerableSet.AddressSet internal executors;

    constructor(address _safe) public {
        safe = GnosisSafe(_safe);
    }

    function addExecutor(address _executor) external {
        require(msg.sender == address(safe));
        executors.add(_executor);
    }

    function removeExecutor(address _executor) external {
        require(msg.sender == address(safe));
        executors.remove(_executor);
    }

    function checkTransaction(
        address to,
        uint256 value,
        bytes memory data,
        Enum.Operation operation,
        uint256 safeTxGas,
        uint256 baseGas,
        uint256 gasPrice,
        address gasToken,
        address payable refundReceiver,
        bytes memory signatures,
        address msgSender
    ) override external {

        // Executors are ok!
        if (executors.contains(msgSender)) {
            return;
        }

        // Owners can exec as well
        address[] memory owners = safe.getOwners();
        for (uint256 i=0 ; i < owners.length ; i++) {
            if (owners[i] == msgSender) {
                return;
            }
        }

        // msg sender is not in the allow list
        revert("msg sender is not allowed to exec");
    }
}
