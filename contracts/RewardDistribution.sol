// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

interface IToken {
    function transfer(address to, uint256 amount) external returns (bool);
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
}

/**
 * @title RewardDistributionEngine
 * @dev Automated token reward distribution for problem solvers
 */
contract RewardDistributionEngine is Ownable, ReentrancyGuard {
    IToken public tokenContract;
    
    // Reward tiers based on difficulty
    mapping(uint256 => uint256) public rewardTiers;
    
    // Solver queue for batch processing
    address[] public pendingRewards;
    mapping(address => uint256) public pendingAmount;
    
    event RewardClaimed(address indexed solver, uint256 amount);
    event BatchDistribution(uint256 count, uint256 totalAmount);
    event TierUpdated(uint256 difficulty, uint256 reward);
    
    constructor(address _tokenContract) {
        tokenContract = IToken(_tokenContract);
        _initializeTiers();
    }
    
    function _initializeTiers() internal {
        // Difficulty 1-3: Low difficulty
        rewardTiers[1] = 50 * 10 ** 18;
        rewardTiers[2] = 75 * 10 ** 18;
        rewardTiers[3] = 100 * 10 ** 18;
        
        // Difficulty 4-7: Medium difficulty
        rewardTiers[4] = 150 * 10 ** 18;
        rewardTiers[5] = 200 * 10 ** 18;
        rewardTiers[6] = 250 * 10 ** 18;
        rewardTiers[7] = 300 * 10 ** 18;
        
        // Difficulty 8-10: High difficulty
        rewardTiers[8] = 400 * 10 ** 18;
        rewardTiers[9] = 500 * 10 ** 18;
        rewardTiers[10] = 750 * 10 ** 18;
    }
    
    /**
     * @dev Queue reward for distribution
     */
    function queueReward(address solver, uint256 difficulty) external onlyOwner {
        require(solver != address(0), "Invalid solver");
        require(rewardTiers[difficulty] > 0, "Invalid difficulty");
        
        uint256 reward = rewardTiers[difficulty];
        
        if (pendingAmount[solver] == 0) {
            pendingRewards.push(solver);
        }
        
        pendingAmount[solver] += reward;
    }
    
    /**
     * @dev Batch distribute all pending rewards
     */
    function distributePendingRewards() external onlyOwner nonReentrant {
        uint256 totalDistributed = 0;
        uint256 count = pendingRewards.length;
        
        for (uint256 i = 0; i < count; i++) {
            address solver = pendingRewards[i];
            uint256 amount = pendingAmount[solver];
            
            if (amount > 0) {
                require(tokenContract.transfer(solver, amount), "Transfer failed");
                totalDistributed += amount;
                
                emit RewardClaimed(solver, amount);
                
                pendingAmount[solver] = 0;
            }
        }
        
        delete pendingRewards;
        emit BatchDistribution(count, totalDistributed);
    }
    
    /**
     * @dev Update reward tier
     */
    function updateRewardTier(uint256 difficulty, uint256 reward) external onlyOwner {
        require(difficulty >= 1 && difficulty <= 10, "Invalid difficulty");
        rewardTiers[difficulty] = reward;
        emit TierUpdated(difficulty, reward);
    }
    
    /**
     * @dev Get pending rewards count
     */
    function getPendingCount() external view returns (uint256) {
        return pendingRewards.length;
    }
}
