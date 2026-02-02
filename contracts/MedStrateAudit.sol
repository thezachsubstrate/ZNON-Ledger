// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract MedStrateAudit is ERC20, Ownable {
    // 9-Sigma Hard-Coded Tiers
    uint256 public constant TIER_1 = 1 * 10**18;
    uint256 public constant TIER_2 = 2500 * 10**18;
    uint256 public constant TIER_3 = 5000 * 10**18;
    uint256 public constant TIER_4 = 25000 * 10**18;
    uint256 public constant TIER_5 = 100000 * 10**18;

    constructor() ERC20("Proof of Logic", "POL") Ownable(msg.sender) {
        _mint(msg.sender, 1000000 * 10**18);
    }

    function settlement(address recipient, uint256 tier) public onlyOwner {
        uint256 amount;
        // Full 5-Tier Logic Check
        if (tier == 1) amount = TIER_1;
        else if (tier == 2) amount = TIER_2;
        else if (tier == 3) amount = TIER_3;
        else if (tier == 4) amount = TIER_4;
        else if (tier == 5) amount = TIER_5;
        else revert("Invalid 9-Sigma Tier");

        _mint(recipient, amount);
    }
}
