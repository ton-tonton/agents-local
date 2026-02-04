---
name: do-it
description: Use this skill for a Rails workflow including planning, implementation, and testing.
---

# Do It - Rails Workflow

Guide for implementing Rails tasks using a TDD workflow covering Planning, Implementation, and Testing.

## Use this skill when

- Implementing tasks in a Rails project
- Following a planning-implementation-testing cycle
- Managing git commits and notes in a Rails environment

## Instructions

Follow this cycle for each task in your plan.

### 1. Planning

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
Write the minimum code in `app/` necessary to pass tests.
- Focus on making tests green, not perfection.
- Avoid premature optimization.

**REFACTOR - Improve Clarity**
With green tests, improve the code.
- Extract common patterns.
- Simplify logic.
- Follow DRY principle
- Ensure tests remain GREEN.

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
