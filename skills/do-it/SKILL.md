---
name: do-it
description: Use this skill for a Rails workflow including planning, implementation, and testing.
---

# Do It - Rails Workflow

Guide for implementing Rails tasks using a TDD workflow covering Planning, Implementation, and Testing.

## Use this skill when

- Implementing tasks in a Rails project
- Following a planning-implementation-testing cycle
- Managing git commits

## Instructions

- Clarify goals, constraints, and required inputs.
- Apply relevant best practices and validate outcomes.
- Follow this cycle for each task in your plan.

### 1. Select Task

**Select & Mark Task**
1. Identify the next pending `[ ]` task from `plan.md`.
2. Update `plan.md` to mark it as in-progress `[~]`.

### 2. Implement (TDD)

**Research & Documentation**
If unsure about syntax or need more information, search documentation using the MCP `context7` server.

**RED - Write Failing Tests**
Define expected behavior with RSpec before implementation.

- Create test file if needed.
- **Happy Path**: Write only 1 test case for success.
- **Error Path**: Write only 1 test case for failure/validation.
- **Edge Cases**: Cover boundaries if needed.
- Run tests - they MUST fail.

```ruby
describe User do
  context "email validation" do
    it "requires valid format" do
      user = User.new(email: "bad-format")
      expect(user).not_to be_valid
      expect(user.errors[:email]).to include("is invalid")
    end

    it "accepts valid format" do
      user = User.new(email: "test@example.com")
      expect(user).to be_valid
    end
  end
end
```

**GREEN - Implement Minimum Code**
Write the minimum code necessary to make tests pass:

- Focus on making tests green, not perfection
- Avoid premature optimization
- Keep implementation simple
- Run tests - they should PASS
- Create a focused commit for the implement

**REFACTOR - Improve Clarity**
With green tests, improve the code.
- Extract common patterns.
- Improve naming
- Remove duplication
- Simplify logic.
- Follow DRY principle
- Ensure tests remain GREEN.
- Create a focused commit for the refactor

### 3. Test & Finalize

**Verify**
- Run full suite: `bundle exec rspec`
- Check style: `bundle exec rubocop`

**Commit & Update**
1. Commit implementation with a message following Conventional Commits (e.g., `feat: ...`, `fix: ...`, `test: ...`).
2. Update `plan.md` to mark the task as complete `[x]` and append the short commit SHA.
   ```markdown
   - [x] **Task 2.1**: Implement user validation `abc1234`
   ```

### 4. Iterate
Return to **Step 1** for the next task.

## Phase Completion Checkpoints

When all tasks in a phase are complete:

1. **Verify Full Suite**:
   ```bash
   bundle exec rspec
   bundle exec rubocop
   ```

## Quality Gates

- **Passing Tests**: All RSpec examples must pass.
- **Style**: No RuboCop offenses.
- **Security**: No hardcoded secrets.

## Error Recovery

### Failed Tests After GREEN

If tests fail after reaching GREEN:

1. Do NOT proceed to REFACTOR
2. Identify which test started failing
3. Check if refactoring broke something
4. Revert to last known GREEN state
5. Re-approach the implementation

## Working with Existing Tests

When modifying code with existing tests:

### Extend, Don't Replace

- Keep existing tests passing
- Add new tests for new behavior
- Update tests only when requirements change

### Test Migration

When refactoring changes test structure:

1. Run existing tests (should pass)
2. Add new tests for refactored code
3. Migrate test cases to new structure
4. Remove old tests only after new tests pass

### Commit Performance

Keep commits atomic:

- One logical change per commit
- Complete thought, not work-in-progress
- Tests should pass after every commit
