Use Case 6. Input Validation and Error Handling
Validate initial stake is positive and within acceptable range
Ensure bet amounts don't exceed current stake
Verify upper limit is greater than lower limit
Handle invalid numerical inputs gracefully
Prevent negative stake values
Validate probability values are between 0 and 1
Key Components:
1. Custom Exception Hierarchy

ValidationException: Base exception with error type, field, and attempted value tracking
StakeValidationException: Specific to stake-related errors
BetValidationException: Specific to bet amount errors
LimitValidationException: Specific to limit boundary errors
ProbabilityValidationException: Specific to probability range errors
2. ValidationErrorType Enum Categorizes all validation errors: STAKE_ERROR, BET_ERROR, LIMIT_ERROR, PROBABILITY_ERROR, NUMERIC_ERROR, RANGE_ERROR, NULL_ERROR

3. ValidationResult Class

Tracks validation success/failure
Collects multiple errors and warnings
Provides detailed reporting
Distinguishes between critical errors and warnings
4. ValidationConfig Class

Configurable validation rules
Min/max ranges for stakes, bets, probabilities
Strict mode option
Allow zero stake option
Centralized configuration management
5. InputValidator Class

Implements all 6 use cases:
Validate Initial Stake: validateInitialStake()
Checks positive value
Validates against min/max range
Handles NaN and Infinity
Prevents negative values
Ensure Bet ≤ Current Stake: validateBetAmount()
Verifies bet doesn't exceed stake
Checks against min/max bet limits
Validates positive values
Verify Upper > Lower Limit: validateLimits()
Ensures proper limit ordering
Validates initial stake is between limits
Checks for negative limits
Handle Invalid Numeric Inputs: parseAndValidateNumeric()
Graceful parsing with try-catch
Handles null, empty, and invalid strings
Detects NaN and Infinity
Provides clear error messages
Prevent Negative Stakes: validateStakeNonNegative()
Strict negative value prevention
Optional zero-stake handling
Strict mode enforcement
Validate Probability (0-1): validateProbability()
Ensures 0.0 ≤ probability ≤ 1.0
Configurable min/max probability ranges
Handles NaN and Infinity
6. SafeInputHandler Class

Interactive console input with validation
Retry loops for invalid inputs
User-friendly prompts
Real-time validation feedback
Key Features:
Exception Hierarchy: Specific exceptions for different error types
Configurable Rules: Centralized validation configuration
Graceful Error Handling: Never crashes, always provides feedback
Multi-level Validation: Individual, comprehensive, and batch validation
Warning vs Error: Distinguishes critical from non-critical issues
Context Preservation: Tracks what field and value caused errors
NaN/Infinity Detection: Handles edge cases in floating-point math
Null Safety: Explicit null checking
Range Validation: Min/max enforcement for all numeric inputs
User-Friendly Messages: Clear, actionable error descriptions
