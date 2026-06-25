---
name: rails-way
description: Version-aware Rails patterns and conventions for Rails 7.x and 8.x. Covers conventions, Hotwire, Active Record, background jobs, caching, testing, security, performance, and deployment. Use when building, modernizing, or reviewing Rails code and you want to follow Rails conventions.
---

# The Rails Way — Version-Aware Patterns

Convention-first Rails for Rails 7.x and 8.x. Convention over configuration, developer
happiness, server-rendered HTML first.

## Always: detect the version first

Before recommending any tool or feature, read `Gemfile.lock` for the Rails and
Ruby versions. Recommendations differ by version — see the table below.

| Concern        | Rails 8.x (default)                     | Rails 7.x                                  |
|----------------|-----------------------------------------|--------------------------------------------|
| Background jobs| Solid Queue (DB-backed)                 | Sidekiq (Redis) or GoodJob (Postgres)      |
| Cache          | Solid Cache (DB-backed)                 | Redis or Memcached                         |
| Action Cable   | Solid Cable (DB-backed)                 | Redis adapter                              |
| Auth           | `rails g authentication` (native)       | Devise or `has_secure_password`            |
| Rate limiting  | native `rate_limit` in controllers      | rack-attack                                |
| Assets         | Propshaft                               | Sprockets or Propshaft                     |
| Deploy         | Kamal 2 + Thruster (HTTP/2, auto-SSL)   | Capistrano, Docker, or PaaS                |
| JS             | Import maps                             | Webpacker (7.0) or Import maps (7.1+)      |

Leverage the Ruby version too: YJIT (3.3+ default), pattern matching (3.1+).

## Core conventions

- Convention over configuration — always prefer the Rails default.
- RESTful resource routing for every resource.
- Skinny controllers, rich models.
- Service object when controller logic grows past a handful of lines.
- Form object for a form that writes to 2+ models (over `accepts_nested_attributes_for`).
- Query object for complex or reused queries.
- Value object with Ruby's `Data` class.
- Concern only for genuinely shared behavior — use sparingly.
- Presenter / Phlex / ViewComponent for view logic.
- `strict_loading` by default to surface N+1 early.

## Hotwire (server-rendered, JS second)

- **Turbo Drive** — SPA-like navigation for free.
- **Turbo Frames** — independent partial page updates; scope to the right granularity.
- **Turbo Streams** — surgical DOM updates; broadcast for real-time.
- **Stimulus** — small, focused controllers for behavior (`data-controller`, `data-action`).
- Morphing for efficient DOM diffs. Progressive enhancement as the default.

## Active Record

- Associations: polymorphic, STI, delegated types — pick the simplest that fits.
- Scopes composed and merged; avoid logic-heavy callbacks.
- `normalizes` for attribute preprocessing; enums; generated/virtual columns.
- Optimize with `includes`/`joins`, `explain`, and `EXPLAIN ANALYZE`.
- Migrations with safety (strong_migrations); index every foreign key and queried column.
- Multi-database and sharding when scale demands it.

## Background jobs

- Offload anything over ~100ms (email, API calls, heavy processing).
- Concurrency controls, uniqueness, retry strategy, recurring tasks.
- Monitor: Mission Control (Solid Queue) or Sidekiq Web UI.

## Caching

- Fragment and Russian-doll caching with `touch`.
- Low-level `Rails.cache`; key versioning; conditional GET with `stale?`.
- HTTP caching headers for public responses.

## Testing

- RSpec or Minitest — both are standard; match the project.
- Model specs (validations, scopes, business logic), request specs (every endpoint),
  system specs (critical user flows with Capybara).
- FactoryBot or Fabrication over heavy fixtures.
- Shared examples/contexts; stub/mock sparingly. Parallel execution for speed.
- Track coverage with SimpleCov, but test behavior — don't game the number.
- No flaky tests tolerated; CI green before merge.

## API development

- API-only mode when there's no server-rendered UI.
- Serialization: jbuilder, Alba, or Blueprinter. Version the API.
- Token auth (JWT, API keys) or OAuth2 (Doorkeeper).
- Pagination (pagy, kaminari). Document with rswag/OpenAPI.

## Security

- Auth: native generator (8.x) or Devise / `has_secure_password` (7.x).
- Strong parameters; filter sensitive params; CSRF; Content Security Policy.
- Prevent SQL injection (parameterized queries) and XSS (output escaping).
- Static analysis with brakeman; gem audit with bundler-audit.
- **Never hardcode secrets** — encrypted credentials or env vars / a secrets manager.

## Performance

- YJIT in production (Ruby 3.3+).
- Catch N+1 with `strict_loading` + bullet/prosopite.
- Counter caches, touch propagation, sensible eager vs lazy loading.
- Connection pooling; CDN for assets and uploads. Aim API responses < 100ms.

## Deployment

- 8.x: Kamal 2 + Thruster, health checks, accessory services.
- 7.x: Capistrano, Docker Compose, or PaaS (Heroku, Render, Fly.io).
- Safe migrations (strong_migrations); zero-downtime deploys; dev/staging/prod parity.
- Error tracking (Sentry/Honeybadger), structured logging (Lograge), feature flags (Flipper).

## Modern ecosystem (reach for when they earn their keep)

Phlex / ViewComponent (+ Lookbook), Pay (payments), Noticed (notifications),
Pundit / Action Policy (authorization), graphql-ruby, dry-gems for functional patterns.
Keep gem dependencies minimal.
