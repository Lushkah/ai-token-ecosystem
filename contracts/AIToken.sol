// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/Pausable.sol";

/**
 * @title AIToken
 * @dev High-security AI Token for problem-solving ecosystem
 */
contract AIToken is ERC20, Ownable, Pausable {
    // Token distribution configuration
    uint256 public constant MAX_SUPPLY = 1_000_000_000 * 10 ** 18;
    uint256 public rewardPerProblem = 100 * 10 ** 18; // Base reward
    
    // Solver tracking
    mapping(address => uint256) public problemsSolved;
    mapping(address => uint256) public totalEarnings;
    
    event ProblemSolved(address indexed solver, uint256 reward);
    event RewardDistributed(address indexed to, uint256 amount);
    
    constructor() ERC20("AI Token", "AIT") {
        _mint(msg.sender, MAX_SUPPLY / 2); // Initial mint
    }
    
    /**
     * @dev Award tokens for solving problems
     * @param solver Address of problem solver
     * @param difficulty Difficulty multiplier (1-10)
     */
    function awardTokens(address solver, uint256 difficulty) external onlyOwner whenNotPaused {
        require(solver != address(0), "Invalid solver");
        require(difficulty > 0 && difficulty <= 10, "Invalid difficulty");
        
        uint256 reward = (rewardPerProblem * difficulty) / 10;
        require(totalSupply() + reward <= MAX_SUPPLY, "Max supply exceeded");
        
        _mint(solver, reward);
        problemsSolved[solver]++;
        totalEarnings[solver] += reward;
        
        emit ProblemSolved(solver, reward);
        emit RewardDistributed(solver, reward);
    }
    
    /**
     * @dev Update reward amount
     */
    function setRewardPerProblem(uint256 newReward) external onlyOwner {
        rewardPerProblem = newReward;
    }
    
    /**
     * @dev Pause/unpause token transfers
     */
    function pause() external onlyOwner {
        _pause();
    }
    
    function unpause() external onlyOwner {
        _unpause();
    }
    
    /**
     * @dev Get solver statistics
     */
    function getSolverStats(address solver) external view returns (uint256 solved, uint256 earnings) {
        return (problemsSolved[solver], totalEarnings[solver]);
    }
}
