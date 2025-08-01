//SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/metatx/ERC2771Context.sol";

contract Escrow is ERC2771Context {
    address public client;
    address public freelancer;
    IERC20 public token; //USDC

    struct Milestone{
        uint256 amount;
        bool isFunded;
        bool isReleased;
    }
    Milestone[] public milestones;
    bool public initialized;

    event MilestoneFunded(uint256 indexed index, uint256 amount);
    event MilestoneReleased(uint256 indexed index, uint256 amount);

    // Constructor for meta transaction deployment with trusted forwarder
    constructor(address trustedForwarder) ERC2771Context(trustedForwarder) {}

    modifier notInitialized() {
        require(!initialized, "Already initialized");
        _;
    }

    // Regular functions that can be called via forwarder
    function createEscrow(
        address _client,
        address _freelancer, 
        address _token,
        uint256[] memory _amounts
    ) external notInitialized {
        client = _client;
        freelancer = _freelancer;
        token = IERC20(_token);

        for(uint256 i = 0; i < _amounts.length; i++) {
            milestones.push(Milestone({
                amount: _amounts[i],
                isFunded: false,
                isReleased: false
            }));
        }
        initialized = true;
    }

    function fundMilestone(uint256 index) external {
        require(_msgSender() == client, "Only client can fund milestones");
        Milestone storage m = milestones[index];
        require(!m.isFunded, "Milestone already funded");
        token.transferFrom(client, address(this), m.amount);
        m.isFunded = true;
        emit MilestoneFunded(index, m.amount);
    }

    function releaseMilestone(uint256 index) external {
        require(_msgSender() == client, "Only client can release milestones");
        Milestone storage m = milestones[index];
        require(m.isFunded && !m.isReleased, "Milestone not funded or already released");
        token.transfer(freelancer, m.amount);
        m.isReleased = true;
        emit MilestoneReleased(index, m.amount);
    }

    function getMilestones() external view returns (Milestone[] memory) {
        return milestones;
    }
}